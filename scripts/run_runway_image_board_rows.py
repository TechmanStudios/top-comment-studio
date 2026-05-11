#!/usr/bin/env python3
"""Submit or check the separate Runway image-board row workflows."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from top_comment_studio.runway.client import RunwayClient
from top_comment_studio.runway.workflows import (
    build_logical_inputs,
    build_node_outputs,
    parse_node_map,
)
from top_comment_studio.schemas import EpisodeRecord
from top_comment_studio.settings import get_settings


DEFAULT_ROW_WORKFLOW_IDS = {
    "row1": "f4ed6cf3-69b0-436b-a37c-82e1a7eeeb46",
    "row2": "06a818f1-6dec-4cae-878d-ceeb6fbd5c2d",
    "row3": "fd051825-a295-4406-a80b-1fbfd8f8b7da",
}
ROW_ENV_NAMES = {
    "row1": "RUNWAY_IMAGE_BOARD_ROW_1_WORKFLOW_ID",
    "row2": "RUNWAY_IMAGE_BOARD_ROW_2_WORKFLOW_ID",
    "row3": "RUNWAY_IMAGE_BOARD_ROW_3_WORKFLOW_ID",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Submit or check the three separate Runway image-board row workflows."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--submit", action="store_true", help="Submit all configured row workflows.")
    mode.add_argument(
        "--status",
        nargs="+",
        metavar="ROW=INVOCATION_ID",
        help="Check existing row invocations, for example row1=abc row2=def row3=ghi.",
    )
    parser.add_argument("--chain", default="main", help="Local chain id under data/local/chains.")
    parser.add_argument("--episode", default="episode_003", help="Local episode id JSON file name.")
    args = parser.parse_args()

    settings = get_settings()
    if not settings.has_runway_secret:
        raise SystemExit("Set RUNWAYML_HACKATHON_API_SECRET before calling Runway.")

    client = RunwayClient(settings)
    if args.submit:
        summaries = submit_rows(client, settings, args.chain, args.episode)
    else:
        summaries = check_rows(client, parse_status_args(args.status or []))

    print(json.dumps(summaries, indent=2))
    return 0


def submit_rows(
    client: RunwayClient,
    settings: Any,
    chain_id: str,
    episode_id: str,
) -> list[dict[str, Any]]:
    record_path = Path("data/local/chains") / chain_id / f"{episode_id}.json"
    record = EpisodeRecord.model_validate(json.loads(record_path.read_text(encoding="utf-8")))
    node_map, issues = parse_node_map(settings.runway_workflow_node_map_json)
    if issues:
        raise SystemExit("\n".join(issues))
    node_outputs = build_node_outputs(build_logical_inputs(record), node_map)

    summaries: list[dict[str, Any]] = []
    for label, workflow_id in configured_row_workflow_ids().items():
        run_response = client.run_workflow(workflow_id, node_outputs)
        invocation_id = run_response.get("id") or run_response.get("workflowInvocationId")
        if not invocation_id:
            summaries.append({"label": label, "workflow_id": workflow_id, "error": "missing id"})
            continue
        status_response = client.retrieve_workflow_invocation(str(invocation_id))
        summaries.append(
            summarize_invocation(label, workflow_id, str(invocation_id), status_response)
        )
    return summaries


def check_rows(client: RunwayClient, invocations: dict[str, str]) -> list[dict[str, Any]]:
    workflow_ids = configured_row_workflow_ids()
    summaries: list[dict[str, Any]] = []
    for label, invocation_id in invocations.items():
        status_response = client.retrieve_workflow_invocation(invocation_id)
        summaries.append(
            summarize_invocation(label, workflow_ids.get(label, ""), invocation_id, status_response)
        )
    return summaries


def configured_row_workflow_ids() -> dict[str, str]:
    return {
        label: os.getenv(ROW_ENV_NAMES[label], default_workflow_id)
        for label, default_workflow_id in DEFAULT_ROW_WORKFLOW_IDS.items()
    }


def parse_status_args(values: list[str]) -> dict[str, str]:
    invocations: dict[str, str] = {}
    for index, value in enumerate(values, start=1):
        if "=" in value:
            label, invocation_id = value.split("=", 1)
        else:
            label = f"row{index}"
            invocation_id = value
        invocations[label.strip()] = invocation_id.strip()
    return invocations


def summarize_invocation(
    label: str,
    workflow_id: str,
    invocation_id: str,
    response: dict[str, Any],
) -> dict[str, Any]:
    output = response.get("output") or {}
    return {
        "label": label,
        "workflow_id": workflow_id,
        "invocation_id": invocation_id,
        "status": response.get("status"),
        "progress_percent": progress_percent(response.get("progress")),
        "output_count": len(output) if isinstance(output, dict) else None,
        "asset_counts": count_assets(output),
        "failure": response.get("failure") or response.get("failureCode") or "",
    }


def progress_percent(progress: Any) -> float | None:
    if progress is None:
        return None
    try:
        return round(float(progress) * 100, 1)
    except (TypeError, ValueError):
        return None


def count_assets(output: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not isinstance(output, dict):
        return counts
    for value in output.values():
        values = value if isinstance(value, list) else [value]
        for item in values:
            url = (
                item.get("url") if isinstance(item, dict) else item if isinstance(item, str) else ""
            )
            kind = classify_url(url)
            counts[kind] = counts.get(kind, 0) + 1
    return counts


def classify_url(url: str) -> str:
    path = urlparse(url).path.lower()
    if path.endswith(".mp4"):
        return "video"
    if path.endswith(".mp3"):
        return "audio"
    if path.endswith((".png", ".jpg", ".jpeg", ".webp")):
        return "image"
    return "other"


if __name__ == "__main__":
    raise SystemExit(main())
