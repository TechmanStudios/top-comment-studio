from typing import Any
import json

from pydantic import BaseModel, ValidationError

from ..schemas import EpisodeRecord, RunwayWorkflowPreview
from ..settings import Settings


WORKFLOW_NAME = "TCS Gen/Veo Director v2"
WORKFLOW_ASPECT_RATIO = "1080:1920"
RUNWAY_VIDEO_MIN_DURATION_SECONDS = 2
RUNWAY_VIDEO_MAX_DURATION_SECONDS = 10
REQUIRED_WORKFLOW_INPUTS = [
    "episode_id",
    "audience_signal",
    "av_director_packet",
    "opening_frame_prompt",
    "motion_prompt",
    "audio_prompt",
    "sync_prompt",
    "duration_seconds",
    "aspect_ratio",
    "safety_status",
]


class WorkflowEndpointPlan(BaseModel):
    registry_url: str
    workflow_name: str = WORKFLOW_NAME
    workflow_id: str = ""
    llm_text_generation: str = "GPT 5.5"
    image_generation: str = "Nano Banana Pro (Gemini 3 Pro Image)"
    video_generation: str = "Gen-4.5 shot studies + Veo 3.1 unified audio-video final"
    preferred_video_model_id: str = "veo3.1"
    preferred_image_model_id: str = "gemini_image3_pro"
    status: str = "planned"


class WorkflowNodeBinding(BaseModel):
    node_id: str
    output_key: str = "prompt"


def describe_workflow_plan(registry_url: str) -> WorkflowEndpointPlan:
    return WorkflowEndpointPlan(registry_url=registry_url)


def build_workflow_preview(record: EpisodeRecord, settings: Settings) -> RunwayWorkflowPreview:
    logical_inputs = build_logical_inputs(record)
    node_map, node_map_issues = parse_node_map(settings.runway_workflow_node_map_json)
    configuration_issues = list(node_map_issues)

    if not settings.has_runway_workflow_id:
        configuration_issues.append("Set RUNWAY_WORKFLOW_ID after publishing the workflow.")

    missing_inputs = [name for name in REQUIRED_WORKFLOW_INPUTS if name not in node_map]
    if missing_inputs:
        configuration_issues.append("Map workflow input nodes for: " + ", ".join(missing_inputs))

    node_outputs = build_node_outputs(logical_inputs, node_map)
    workflow_id = settings.runway_workflow_id if settings.has_runway_workflow_id else ""
    return RunwayWorkflowPreview(
        workflow_id=workflow_id,
        workflow_name=settings.runway_workflow_name or WORKFLOW_NAME,
        endpoint_path=f"/v1/workflows/{workflow_id}" if workflow_id else "",
        duration_seconds=int(logical_inputs["duration_seconds"]),
        aspect_ratio=str(logical_inputs["aspect_ratio"]),
        logical_inputs=logical_inputs,
        node_outputs=node_outputs,
        configuration_issues=configuration_issues,
        can_submit=not configuration_issues,
    )


def build_logical_inputs(record: EpisodeRecord) -> dict[str, str]:
    context = record.production_context
    packet = record.package.av_director_packet
    return {
        "episode_id": record.episode_id,
        "audience_signal": packet.audience_signal or str(record.source_comment.get("text", "")),
        "av_director_packet": json.dumps(packet.model_dump(), ensure_ascii=True),
        "opening_frame_prompt": packet.visual_anchor,
        "motion_prompt": " ".join([packet.motion_arc, packet.camera_language]).strip(),
        "audio_prompt": packet.audio_design,
        "sync_prompt": packet.audio_visual_sync,
        "duration_seconds": str(clamp_runway_video_duration(context.target_duration_seconds)),
        "aspect_ratio": WORKFLOW_ASPECT_RATIO,
        "safety_status": record.guardrail.status,
    }


def clamp_runway_video_duration(duration_seconds: int) -> int:
    return min(
        max(duration_seconds, RUNWAY_VIDEO_MIN_DURATION_SECONDS),
        RUNWAY_VIDEO_MAX_DURATION_SECONDS,
    )


def parse_node_map(raw_node_map: str) -> tuple[dict[str, WorkflowNodeBinding], list[str]]:
    if not raw_node_map.strip() or raw_node_map.strip() == "{}":
        return {}, []

    try:
        raw_data = json.loads(raw_node_map)
    except json.JSONDecodeError as exc:
        return {}, [f"RUNWAY_WORKFLOW_NODE_MAP_JSON is not valid JSON: {exc.msg}."]

    if not isinstance(raw_data, dict):
        return {}, ["RUNWAY_WORKFLOW_NODE_MAP_JSON must be a JSON object."]

    node_map: dict[str, WorkflowNodeBinding] = {}
    issues: list[str] = []
    for input_name, binding_data in raw_data.items():
        try:
            node_map[input_name] = WorkflowNodeBinding.model_validate(binding_data)
        except ValidationError as exc:
            issues.append(f"Invalid node map entry for {input_name}: {exc.errors()[0]['msg']}.")
    return node_map, issues


def build_node_outputs(
    logical_inputs: dict[str, str | int | bool],
    node_map: dict[str, WorkflowNodeBinding],
) -> dict[str, dict[str, dict[str, Any]]]:
    node_outputs: dict[str, dict[str, dict[str, Any]]] = {}
    for input_name, input_value in logical_inputs.items():
        binding = node_map.get(input_name)
        if binding is None:
            continue
        node_outputs.setdefault(binding.node_id, {})[binding.output_key] = {
            "type": "primitive",
            "value": input_value,
        }
    return node_outputs


def workflow_submission_blockers(
    record: EpisodeRecord,
    preview: RunwayWorkflowPreview,
    *,
    has_runway_secret: bool,
    creator_approved: bool,
) -> list[str]:
    blockers: list[str] = []
    if not creator_approved:
        blockers.append("Creator approval is required before submitting to Runway.")
    if record.guardrail.status == "rejected":
        blockers.append("Rejected comments cannot be submitted to Runway.")
    if not has_runway_secret:
        blockers.append("Set RUNWAYML_HACKATHON_API_SECRET before submitting to Runway.")
    blockers.extend(preview.configuration_issues)
    return blockers
