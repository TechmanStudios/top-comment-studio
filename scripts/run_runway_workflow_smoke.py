#!/usr/bin/env python3
"""Run a paid smoke test against a published Runway Workflow endpoint."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import httpx

from top_comment_studio.app import create_episode_record
from top_comment_studio.runway.client import RunwayClient, RunwayClientError
from top_comment_studio.runway.workflows import (
    REQUIRED_WORKFLOW_INPUTS,
    WorkflowNodeBinding,
    build_logical_inputs,
    build_node_outputs,
)
from top_comment_studio.schemas import CommentInput
from top_comment_studio.settings import get_settings


DEFAULT_COMMENT = "Make the AI build a floating city powered by storms."
DEFAULT_OUTPUT_DIR = Path("data/local/runway_outputs")


def main() -> int:
    args = parse_args()
    client = RunwayClient(get_settings())

    try:
        graph = client.retrieve_workflow(args.workflow_id)["graph"]
    except (KeyError, RunwayClientError) as exc:
        print(f"Could not retrieve workflow {args.workflow_id}: {exc}", file=sys.stderr)
        return 1

    nodes_by_name = {
        node.get("nodeProps", {}).get("name", ""): node for node in graph.get("nodes", [])
    }
    try:
        node_map = {
            name: WorkflowNodeBinding(
                node_id=str(nodes_by_name[f"TCS Input: {name}"]["id"]),
                output_key="prompt",
            )
            for name in REQUIRED_WORKFLOW_INPUTS
        }
    except KeyError as exc:
        print(f"Published graph is missing a required TCS input node: {exc}", file=sys.stderr)
        return 1

    record = create_episode_record(build_comment_input(args.comment))
    logical_inputs = build_logical_inputs(record)
    node_outputs = build_node_outputs(logical_inputs, node_map)

    print(f"Submitting paid smoke to workflow {args.workflow_id}")
    print(f"nodeOutputs: {len(node_outputs)} TCS inputs")
    print(f"audience_signal: {logical_inputs['audience_signal']}")
    print(
        "subject_focus: "
        + str(json.loads(str(logical_inputs["av_director_packet"]))["subject_focus"])
    )

    try:
        submission = client.run_workflow(args.workflow_id, node_outputs)
    except RunwayClientError as exc:
        print(f"Submit failed: {exc} status={exc.status_code}", file=sys.stderr)
        print(exc.response_body[:1200], file=sys.stderr)
        return 1

    invocation_id = str(submission.get("id") or submission.get("invocationId") or "")
    if not invocation_id:
        print("Runway did not return an invocation id.", file=sys.stderr)
        print(json.dumps(_without_output(submission), indent=2)[:2000], file=sys.stderr)
        return 1
    print(f"invocation_id: {invocation_id}")

    invocation = poll_invocation(client, invocation_id, args.poll_seconds, args.max_polls)
    if invocation is None:
        return 1

    status = invocation.get("status")
    print(f"final_status: {status}")
    print_node_errors(invocation)
    if status != "SUCCEEDED":
        print(json.dumps(_without_output(invocation), indent=2)[:4000], file=sys.stderr)
        return 1

    video_urls = [
        (label, url)
        for label, url in collect_urls(invocation.get("output") or {})
        if ".mp4" in url.split("?", 1)[0].lower()
    ]
    print(f"outputs_found: video={len(video_urls)}")
    if not video_urls:
        print("No MP4 output URL found.", file=sys.stderr)
        return 1

    downloaded = download_videos(video_urls, args.output_dir, invocation_id)
    result_path = args.output_dir / f"{invocation_id}_result.json"
    result_path.write_text(
        json.dumps(
            {
                "workflow_id": args.workflow_id,
                "invocation_id": invocation_id,
                "status": status,
                "progress": invocation.get("progress"),
                "nodeErrors": invocation.get("nodeErrors") or {},
                "output_labels": [label for label, _ in video_urls],
                "downloaded": [str(path) for path in downloaded],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"saved_result: {result_path}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("workflow_id", help="Published Runway Workflow endpoint UUID.")
    parser.add_argument("--comment", default=DEFAULT_COMMENT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--max-polls", type=int, default=90)
    return parser.parse_args()


def build_comment_input(comment: str) -> CommentInput:
    return CommentInput(
        selected_comment=comment,
        author_display_name="@stormbuilder",
        like_count=428,
        creative_notes=(
            "Keep the floating city as the primary subject from the first beat; use any guide "
            "character only as a tiny scale cue, never as the hero."
        ),
        subject_focus=(
            "One recognizable storm-powered floating city silhouette remains the hero from hook "
            "to payoff."
        ),
        scene_world=(
            "A fictional sky world of storm clouds, suspended architecture, turbines, lightning "
            "collectors, and clean vertical scale cues."
        ),
        motion_direction=(
            "Storm energy gathers around the city, turbines awaken, the city lifts, and the final "
            "beat lands on a clear floating-city reveal."
        ),
        camera_direction=(
            "Vertical cinematic push-in toward the city, stable subject tracking, wide-to-closer "
            "reveal, no chaotic cutting."
        ),
        audio_direction=(
            "Native storm ambience, low turbine whine, lightning crackle, heavy lift swell, and a "
            "clean payoff hit synced to the city reveal."
        ),
        quality_constraints=(
            "No captions, no logos, no copyrighted characters, no real-person likeness, no graphic "
            "harm, no unsafe instructions."
        ),
    )


def poll_invocation(
    client: RunwayClient, invocation_id: str, poll_seconds: int, max_polls: int
) -> dict[str, Any] | None:
    for poll_index in range(max_polls):
        try:
            invocation = client.retrieve_workflow_invocation(invocation_id)
        except RunwayClientError as exc:
            print(f"Poll failed: {exc} status={exc.status_code}", file=sys.stderr)
            print(exc.response_body[:1200], file=sys.stderr)
            return None

        status = str(invocation.get("status", ""))
        progress = invocation.get("progress")
        if (
            poll_index == 0
            or poll_index % 2 == 0
            or status
            in {
                "SUCCEEDED",
                "FAILED",
                "CANCELLED",
            }
        ):
            print(f"poll {poll_index:02d}: status={status} progress={progress}")
            print_node_errors(invocation)
            sys.stdout.flush()
        if status in {"SUCCEEDED", "FAILED", "CANCELLED"}:
            return invocation
        time.sleep(poll_seconds)

    print("Timed out waiting for workflow invocation to finish.", file=sys.stderr)
    return None


def print_node_errors(invocation: dict[str, Any]) -> None:
    node_errors = invocation.get("nodeErrors") or {}
    if not node_errors:
        return
    print("nodeErrors:")
    for node_id, error in node_errors.items():
        if isinstance(error, dict):
            print(f"- {error.get('nodeName', node_id)}: {error.get('message', error)}")
        else:
            print(f"- {node_id}: {error}")


def collect_urls(value: Any) -> list[tuple[str, str]]:
    urls: list[tuple[str, str]] = []
    if isinstance(value, str) and value.startswith("http"):
        urls.append(("output", value))
    elif isinstance(value, list):
        for index, item in enumerate(value, start=1):
            for label, url in collect_urls(item):
                suffix = "" if label == "output" else f"_{label}"
                urls.append((f"item_{index}{suffix}", url))
    elif isinstance(value, dict):
        for key, item in value.items():
            for label, url in collect_urls(item):
                suffix = "" if label == "output" else f"_{label}"
                urls.append((f"{key}{suffix}", url))
    return urls


def download_videos(
    video_urls: list[tuple[str, str]], output_dir: Path, invocation_id: str
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[Path] = []
    with httpx.Client(timeout=300) as http_client:
        for index, (label, url) in enumerate(video_urls, start=1):
            file_path = output_dir / f"{invocation_id}_{clean_filename(label)}.mp4"
            response = http_client.get(url)
            response.raise_for_status()
            file_path.write_bytes(response.content)
            downloaded.append(file_path)
            print(f"downloaded_video_{index}: {file_path} bytes={file_path.stat().st_size}")
    return downloaded


def clean_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")
    return value[:120] or "output"


def _without_output(payload: dict[str, Any]) -> dict[str, Any]:
    safe = dict(payload)
    safe.pop("output", None)
    return safe


if __name__ == "__main__":
    raise SystemExit(main())
