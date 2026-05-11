#!/usr/bin/env python3
"""Verify the published Runway workflow contract used by Top Comment Studio."""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from typing import Any

from top_comment_studio.runway.client import RunwayClient, RunwayClientError
from top_comment_studio.runway.workflows import REQUIRED_WORKFLOW_INPUTS, parse_node_map
from top_comment_studio.settings import get_settings


EXPECTED_INPUT_DEFAULTS = {
    "episode_id": "episode_001",
    "audience_signal": "Make the AI build a floating city powered by storms.",
    "av_director_packet": (
        '{"audience_signal":"Make the AI build a floating city powered by storms.",'
        '"creator_intent":"A safe fictional storm-powered floating city reveal.",'
        '"subject_focus":"One recognizable floating city silhouette from hook to payoff.",'
        '"scene_world":"Fictional sky world with storm clouds, clean scale cues, and '
        'readable structures.",'
        '"visual_anchor":"Bold 9:16 opening frame with a readable storm-powered floating city.",'
        '"motion_arc":"Storm energy gathers, lifts the city, and resolves in a clear payoff '
        'pose.",'
        '"camera_language":"Vertical cinematic push-in with stable subject tracking.",'
        '"audio_design":"Native storm ambience, turbine whine, transformation accent, payoff hit.",'
        '"audio_visual_sync":"Lock each sound event to a visible cause and land the final hit '
        'on the payoff frame.",'
        '"negative_constraints":"No captions, logos, copyrighted characters, real-person likeness, '
        'graphic harm, or unsafe instructions."}'
    ),
    "opening_frame_prompt": (
        "A bold 9:16 opening frame where the storm-powered floating city reads within one second."
    ),
    "motion_prompt": (
        "Readable hook, physical storm-energy transformation, smooth reveal, clear payoff pose."
    ),
    "audio_prompt": "Native storm ambience, turbine whine, transformation accent, payoff hit.",
    "sync_prompt": "Lock each sound event to a visible cause and land the final hit on the payoff frame.",
    "duration_seconds": "4",
    "aspect_ratio": "1080:1920",
    "safety_status": "approved",
}

COMBINE_INPUT_ORDER = [
    "episode_id",
    "duration_seconds",
    "aspect_ratio",
    "safety_status",
    "audience_signal",
    "av_director_packet",
    "opening_frame_prompt",
    "motion_prompt",
    "audio_prompt",
    "sync_prompt",
]

COMBINE_NODE_NAMES = [
    "TCS Combine 01: episode + duration",
    "TCS Combine 02: + aspect ratio",
    "TCS Combine 03: + safety",
    "TCS Combine 04: + audience signal",
    "TCS Combine 05: + AV director packet",
    "TCS Combine 06: + opening frame",
    "TCS Combine 07: + motion",
    "TCS Combine 08: + native audio",
    "TCS Combine 09: + sync",
]

BOARD_NODES = [
    "TCS Board 01: hook frame",
    "TCS Board 02: identity frame",
    "TCS Board 03: world detail",
    "TCS Board 04: cause frame",
    "TCS Board 05: transformation frame",
    "TCS Board 06: camera study",
    "TCS Board 07: sound-source frame",
    "TCS Board 08: payoff frame",
    "TCS Board 09: hero poster",
]

SEGMENT_NODES = [
    "TCS Long Final Segment 01: Veo 3.1 native audio",
    "TCS Long Final Segment 02: Veo 3.1 native audio",
    "TCS Long Final Segment 03: Veo 3.1 native audio",
    "TCS Long Final Segment 04: Veo 3.1 native audio",
]

STORYBOARD_FRAME_NODES = [
    "TCS Storyboard Frame 01: hook",
    "TCS Storyboard Frame 02: escalation",
    "TCS Storyboard Frame 03: transformation",
    "TCS Storyboard Frame 04: payoff",
]

STORYBOARD_SEGMENT_NODES = [
    "TCS Storyboard Segment 01: hook native audio",
    "TCS Storyboard Segment 02: escalation native audio",
    "TCS Storyboard Segment 03: transformation native audio",
    "TCS Storyboard Segment 04: payoff native audio",
]

PHOTO_ENHANCER_SHARED_NODES = {
    "validator": "TCS Photo Enhancer: validator brain",
    "question": "TCS Photo Enhancer: frame question",
    "extractor": "TCS Photo Enhancer: prompt extractor",
}

PHOTO_ENHANCER_STEP_SUFFIXES = {
    "analysis_1": "analysis pass 1",
    "prompt_1": "prompt pass 1",
    "first_pass": "first pass image",
    "analysis_2": "analysis pass 2",
    "prompt_2": "prompt pass 2",
    "final_image": "final enhanced frame",
}

VIDEO_IMAGE_INPUT_CANDIDATES = {
    "promptImage",
    "prompt_image",
    "referenceImages",
    "reference_images",
    "image",
    "startFrame",
    "start_frame",
    "firstFrame",
}


def main() -> int:
    args = set(sys.argv[1:])
    strict_defaults = "--strict-defaults" in args
    require_final_master = "--require-final-master" in args
    require_storyboard_to_short = "--require-storyboard-to-short" in args
    require_continuity_core = "--require-continuity-core" in args
    require_photo_enhancer_chains = "--require-photo-enhancer-chains" in args
    require_seamless_transition_keyframes = "--require-seamless-transition-keyframes" in args
    require_1080p_video = "--require-1080p-video" in args
    errors: list[str] = []
    warnings: list[str] = []

    selected_modes = [require_final_master, require_storyboard_to_short, require_continuity_core]
    if sum(1 for selected_mode in selected_modes if selected_mode) > 1:
        errors.append(
            "Choose only one graph mode: --require-final-master, --require-storyboard-to-short, "
            "or --require-continuity-core."
        )
    if require_photo_enhancer_chains and not (
        require_storyboard_to_short or require_continuity_core
    ):
        errors.append(
            "--require-photo-enhancer-chains must be combined with "
            "--require-storyboard-to-short or --require-continuity-core."
        )
    if require_seamless_transition_keyframes and not require_photo_enhancer_chains:
        errors.append(
            "--require-seamless-transition-keyframes must be combined with "
            "--require-photo-enhancer-chains."
        )

    unknown_args = args - {
        "--strict-defaults",
        "--require-final-master",
        "--require-storyboard-to-short",
        "--require-continuity-core",
        "--require-photo-enhancer-chains",
        "--require-seamless-transition-keyframes",
        "--require-1080p-video",
    }
    for unknown_arg in sorted(unknown_args):
        errors.append(f"Unknown argument: {unknown_arg}")

    settings = get_settings()
    if not settings.has_runway_secret:
        errors.append("Set RUNWAYML_HACKATHON_API_SECRET before verifying the live workflow.")
    if not settings.has_runway_workflow_id:
        errors.append("Set RUNWAY_WORKFLOW_ID before verifying the live workflow.")
    if errors:
        print_report(settings.runway_workflow_id, [], [], warnings, errors)
        return 1

    node_map, node_map_issues = parse_node_map(settings.runway_workflow_node_map_json)
    errors.extend(node_map_issues)
    errors.extend(validate_node_map(node_map))
    if errors:
        print_report(settings.runway_workflow_id, [], [], warnings, errors)
        return 1

    try:
        graph = RunwayClient(settings).retrieve_workflow(settings.runway_workflow_id)["graph"]
    except (KeyError, RunwayClientError) as exc:
        errors.append(f"Could not retrieve workflow graph: {exc}")
        print_report(settings.runway_workflow_id, [], [], warnings, errors)
        return 1

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    nodes_by_id = {str(node.get("id")): node for node in nodes}
    nodes_by_name = index_nodes_by_name(nodes, errors)

    input_lines, input_warnings = validate_input_nodes(node_map, nodes_by_id)
    warnings.extend(input_warnings)
    if strict_defaults:
        errors.extend(input_warnings)

    mode_lines: list[str] = []
    errors.extend(
        validate_director_chain(
            node_map,
            nodes_by_name,
            edges,
            require_claude_director=require_continuity_core or not require_storyboard_to_short,
            require_preview_video=not (require_storyboard_to_short or require_continuity_core),
        )
    )
    if require_continuity_core:
        mode_lines, mode_errors = validate_continuity_core(nodes_by_name, edges)
        errors.extend(mode_errors)
        storyboard_lines, storyboard_errors = validate_storyboard_to_short(
            nodes_by_name,
            edges,
            prompt_source_node_name="TCS Continuity Core: enriched creative brief",
            require_photo_enhancer_chains=require_photo_enhancer_chains,
            require_seamless_transition_keyframes=require_seamless_transition_keyframes,
            require_1080p_video=require_1080p_video,
        )
        mode_lines.extend(storyboard_lines)
        errors.extend(storyboard_errors)
    elif require_storyboard_to_short:
        mode_lines, mode_errors = validate_storyboard_to_short(
            nodes_by_name,
            edges,
            require_photo_enhancer_chains=require_photo_enhancer_chains,
            require_seamless_transition_keyframes=require_seamless_transition_keyframes,
            require_1080p_video=require_1080p_video,
        )
        errors.extend(mode_errors)
    elif require_final_master:
        mode_lines, mode_errors = validate_final_master(nodes_by_name, edges)
        errors.extend(mode_errors)

    print_report(settings.runway_workflow_id, input_lines, mode_lines, warnings, errors)
    return 1 if errors else 0


def validate_node_map(node_map: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing_inputs = [name for name in REQUIRED_WORKFLOW_INPUTS if name not in node_map]
    if missing_inputs:
        errors.append("Missing node-map entries: " + ", ".join(missing_inputs))

    id_counts = Counter(binding.node_id for binding in node_map.values())
    duplicate_ids = sorted(node_id for node_id, count in id_counts.items() if count > 1)
    for duplicate_id in duplicate_ids:
        names = sorted(
            name for name, binding in node_map.items() if binding.node_id == duplicate_id
        )
        errors.append(f"Node id {duplicate_id} is mapped to multiple inputs: {', '.join(names)}")
    return errors


def validate_input_nodes(
    node_map: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]]
) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    warnings: list[str] = []
    default_values: dict[str, str] = {}

    for input_name in REQUIRED_WORKFLOW_INPUTS:
        binding = node_map.get(input_name)
        if binding is None:
            continue
        node = nodes_by_id.get(binding.node_id)
        if node is None:
            warnings.append(f"{input_name} maps to missing graph node {binding.node_id}.")
            continue

        expected_name = f"TCS Input: {input_name}"
        actual_name = node_name(node)
        output = node.get("nodeOutputs", {}).get(binding.output_key, {})
        label = output.get("label", "")
        value = str(output.get("value", ""))
        default_values[input_name] = value

        if actual_name != expected_name:
            warnings.append(
                f"{input_name} node name is {actual_name!r}; expected {expected_name!r}."
            )
        if label != expected_name:
            warnings.append(f"{input_name} output label is {label!r}; expected {expected_name!r}.")
        if output.get("exposedToApp") is not True:
            warnings.append(
                f"{input_name} output {binding.output_key!r} is not exposed to the app."
            )
        expected_default = EXPECTED_INPUT_DEFAULTS[input_name]
        if value != expected_default:
            warnings.append(
                f"{input_name} canvas default is {value!r}; expected {expected_default!r}."
            )

        lines.append(f"{input_name}: {binding.node_id} -> {actual_name} = {value!r}")

    unique_defaults = set(default_values.values())
    if len(default_values) > 1 and len(unique_defaults) == 1:
        warnings.append(
            "All TCS input canvas defaults are identical. App API submissions override them, "
            "but manual Runway runs and visual inspection will be misleading."
        )
    return lines, warnings


def validate_director_chain(
    node_map: dict[str, Any],
    nodes_by_name: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
    *,
    require_claude_director: bool,
    require_preview_video: bool,
) -> list[str]:
    errors: list[str] = []
    edge_keys = build_edge_keys(edges)

    combine_nodes = [nodes_by_name.get(name) for name in COMBINE_NODE_NAMES]
    for combine_name, combine_node in zip(COMBINE_NODE_NAMES, combine_nodes, strict=True):
        validate_named_node(combine_node, combine_name, "text-concat", errors)
    if any(combine_node is None for combine_node in combine_nodes):
        return errors

    require_edge(
        edge_keys,
        node_map[COMBINE_INPUT_ORDER[0]].node_id,
        "prompt",
        str(combine_nodes[0]["id"]),
        "strings",
        0,
        errors,
    )
    require_edge(
        edge_keys,
        node_map[COMBINE_INPUT_ORDER[1]].node_id,
        "prompt",
        str(combine_nodes[0]["id"]),
        "strings",
        1,
        errors,
    )

    for order_index in range(2, len(COMBINE_INPUT_ORDER)):
        previous_combine = combine_nodes[order_index - 2]
        current_combine = combine_nodes[order_index - 1]
        input_name = COMBINE_INPUT_ORDER[order_index]
        require_edge(
            edge_keys,
            str(previous_combine["id"]),
            "text",
            str(current_combine["id"]),
            "strings",
            0,
            errors,
        )
        require_edge(
            edge_keys,
            node_map[input_name].node_id,
            "prompt",
            str(current_combine["id"]),
            "strings",
            1,
            errors,
        )

    if not require_claude_director:
        return errors

    validate_named_node(
        nodes_by_name.get("TCS Director: Claude Veo prompt"),
        "TCS Director: Claude Veo prompt",
        "claude",
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        COMBINE_NODE_NAMES[-1],
        "text",
        "TCS Director: Claude Veo prompt",
        "prompt",
        None,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        "TCS Director: system_prompt",
        "prompt",
        "TCS Director: Claude Veo prompt",
        "system_prompt",
        None,
        errors,
    )
    if require_preview_video:
        validate_named_node(
            nodes_by_name.get("TCS Final: Veo 3.1 native audio video"),
            "TCS Final: Veo 3.1 native audio video",
            "veo-3.1",
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            "TCS Director: Claude Veo prompt",
            "text",
            "TCS Final: Veo 3.1 native audio video",
            "text_prompt",
            None,
            errors,
        )
        validate_veo_node(
            nodes_by_name.get("TCS Final: Veo 3.1 native audio video"),
            "TCS Final: Veo 3.1 native audio video",
            expected_route="t2v",
            errors=errors,
        )
    return errors


def validate_final_master(
    nodes_by_name: dict[str, dict[str, Any]], edges: list[dict[str, Any]]
) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    errors: list[str] = []
    edge_keys = build_edge_keys(edges)

    validate_named_node(
        nodes_by_name.get("TCS Asset Planner: board/sidecar/segments JSON"),
        "TCS Asset Planner: board/sidecar/segments JSON",
        "claude",
        errors,
    )
    validate_named_node(
        nodes_by_name.get("TCS Asset Parser: boards sidecars segments"),
        "TCS Asset Parser: boards sidecars segments",
        "json-parse",
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        COMBINE_NODE_NAMES[-1],
        "text",
        "TCS Asset Planner: board/sidecar/segments JSON",
        "prompt",
        None,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        "TCS Asset Planner: system_prompt",
        "prompt",
        "TCS Asset Planner: board/sidecar/segments JSON",
        "system_prompt",
        None,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        "TCS Asset Planner: board/sidecar/segments JSON",
        "text",
        "TCS Asset Parser: boards sidecars segments",
        "text",
        None,
        errors,
    )

    parser = nodes_by_name.get("TCS Asset Parser: boards sidecars segments")
    expected_paths = [f"board_prompts.{index}" for index in range(9)]
    expected_paths.extend(f"sidecar_prompts.{index}" for index in range(3))
    expected_paths.extend(f"segment_prompts.{index}" for index in range(4))
    validate_parser_paths(
        parser, "TCS Asset Parser: boards sidecars segments", expected_paths, errors
    )

    for index, board_name in enumerate(BOARD_NODES):
        board = nodes_by_name.get(board_name)
        validate_named_node(board, board_name, "gemini-image-3-pro", errors)
        validate_gemini_image_node(board, board_name, errors)
        require_parser_edge(parser, board, index, "text_prompt", edge_keys, errors)
        lines.append(f"board {index + 1}: {board_name}")

    for index, segment_name in enumerate(SEGMENT_NODES):
        segment = nodes_by_name.get(segment_name)
        validate_veo_node(segment, segment_name, expected_route="t2v", errors=errors)
        require_parser_edge(parser, segment, 12 + index, "text_prompt", edge_keys, errors)
        lines.append(f"veo segment {index + 1}: {segment_name}")

    require_named_edge(
        edge_keys,
        nodes_by_name,
        SEGMENT_NODES[0],
        "video",
        "TCS Stitch A: segments 01+02",
        "input",
        0,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        SEGMENT_NODES[1],
        "video",
        "TCS Stitch A: segments 01+02",
        "input",
        1,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        SEGMENT_NODES[2],
        "video",
        "TCS Stitch B: segments 03+04",
        "input",
        0,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        SEGMENT_NODES[3],
        "video",
        "TCS Stitch B: segments 03+04",
        "input",
        1,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        "TCS Stitch A: segments 01+02",
        "video",
        "TCS Long Final: stitched 16s native audio",
        "input",
        0,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        "TCS Stitch B: segments 03+04",
        "video",
        "TCS Long Final: stitched 16s native audio",
        "input",
        1,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        "TCS Final: Veo 3.1 native audio video",
        "video",
        "TCS Final Final: director + asset master",
        "input",
        0,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        "TCS Long Final: stitched 16s native audio",
        "video",
        "TCS Final Final: director + asset master",
        "input",
        1,
        errors,
    )
    validate_single_exposed_generated_output(
        nodes_by_name.values(), "final_final_video_20s", errors
    )
    lines.append("final output: final_final_video_20s")
    return lines, errors


def validate_continuity_core(
    nodes_by_name: dict[str, dict[str, Any]], edges: list[dict[str, Any]]
) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    errors: list[str] = []
    edge_keys = build_edge_keys(edges)

    director_name = "TCS Director: Claude Veo prompt"
    asset_planner_name = "TCS Asset Planner: board/sidecar/segments JSON"
    asset_parser_name = "TCS Asset Parser: boards sidecars segments"
    asset_map_name = "TCS Asset Planner: parsed creative map"
    continuity_intake_name = "TCS Continuity Core: enriched creative brief"

    validate_named_node(nodes_by_name.get(director_name), director_name, "claude", errors)
    validate_named_node(nodes_by_name.get(asset_planner_name), asset_planner_name, "claude", errors)
    validate_named_node(
        nodes_by_name.get(asset_parser_name), asset_parser_name, "json-parse", errors
    )
    validate_named_node(nodes_by_name.get(asset_map_name), asset_map_name, "text-concat", errors)
    validate_named_node(
        nodes_by_name.get(continuity_intake_name), continuity_intake_name, "text-concat", errors
    )

    require_named_edge(
        edge_keys,
        nodes_by_name,
        "TCS Director: system_prompt",
        "prompt",
        director_name,
        "system_prompt",
        None,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        COMBINE_NODE_NAMES[-1],
        "text",
        director_name,
        "prompt",
        None,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        "TCS Asset Planner: system_prompt",
        "prompt",
        asset_planner_name,
        "system_prompt",
        None,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        COMBINE_NODE_NAMES[-1],
        "text",
        asset_planner_name,
        "prompt",
        None,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        asset_planner_name,
        "text",
        asset_parser_name,
        "text",
        None,
        errors,
    )

    require_named_edge(
        edge_keys,
        nodes_by_name,
        COMBINE_NODE_NAMES[-1],
        "text",
        continuity_intake_name,
        "strings",
        0,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        director_name,
        "text",
        continuity_intake_name,
        "strings",
        1,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        asset_map_name,
        "text",
        continuity_intake_name,
        "strings",
        2,
        errors,
    )

    asset_parser = nodes_by_name.get(asset_parser_name)
    expected_asset_paths = [f"board_prompts.{index}" for index in range(9)]
    expected_asset_paths.extend(f"sidecar_prompts.{index}" for index in range(3))
    expected_asset_paths.extend(f"segment_prompts.{index}" for index in range(4))
    expected_asset_paths.append("continuity_notes")
    validate_parser_paths(asset_parser, asset_parser_name, expected_asset_paths, errors)

    asset_map = nodes_by_name.get(asset_map_name)
    for parser_index in range(17):
        require_parser_edge(
            asset_parser,
            asset_map,
            parser_index,
            "strings",
            edge_keys,
            errors,
            target_index=parser_index,
        )

    lines.extend(
        [
            "outer director: Claude creative treatment",
            "outer asset planner: board/sidecar/segment JSON",
            "outer asset parser: parsed creative map",
            "continuity core intake: raw brief + director treatment + parsed asset map",
        ]
    )
    return lines, errors


def validate_storyboard_to_short(
    nodes_by_name: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
    *,
    prompt_source_node_name: str = COMBINE_NODE_NAMES[-1],
    require_photo_enhancer_chains: bool = False,
    require_seamless_transition_keyframes: bool = False,
    require_1080p_video: bool = False,
) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    errors: list[str] = []
    edge_keys = build_edge_keys(edges)

    planner_name = "TCS Storyboard Director: continuity JSON"
    parser_name = "TCS Storyboard Parser: continuity JSON"
    anchor_name = "TCS Storyboard Anchor: identity/world reference"
    final_name = "TCS Storyboard Final: stitched 16s short"

    validate_named_node(nodes_by_name.get(planner_name), planner_name, "claude", errors)
    validate_named_node(nodes_by_name.get(parser_name), parser_name, "json-parse", errors)
    require_named_edge(
        edge_keys,
        nodes_by_name,
        prompt_source_node_name,
        "text",
        planner_name,
        "prompt",
        None,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        "TCS Storyboard Director: system_prompt",
        "prompt",
        planner_name,
        "system_prompt",
        None,
        errors,
    )
    require_named_edge(
        edge_keys,
        nodes_by_name,
        planner_name,
        "text",
        parser_name,
        "text",
        None,
        errors,
    )

    parser = nodes_by_name.get(parser_name)
    expected_paths = ["identity_anchor_prompt"]
    expected_paths.extend(f"board_prompts.{index}" for index in range(4))
    expected_paths.extend(f"segment_prompts.{index}" for index in range(4))
    expected_paths.append("continuity_rules")
    validate_parser_paths(parser, parser_name, expected_paths, errors)

    anchor = nodes_by_name.get(anchor_name)
    validate_named_node(anchor, anchor_name, "gemini-image-3-pro", errors)
    validate_gemini_image_node(anchor, anchor_name, errors)
    require_parser_edge(parser, anchor, 0, "text_prompt", edge_keys, errors)
    lines.append("anchor: identity/world reference image")

    for index, frame_name in enumerate(STORYBOARD_FRAME_NODES):
        frame = nodes_by_name.get(frame_name)
        validate_named_node(frame, frame_name, "gemini-image-3-pro", errors)
        validate_gemini_image_node(frame, frame_name, errors)
        require_parser_edge(parser, frame, index + 1, "text_prompt", edge_keys, errors)
        if anchor is not None and frame is not None:
            require_edge(
                edge_keys,
                str(anchor["id"]),
                "image",
                str(frame["id"]),
                "reference_images",
                0,
                errors,
            )
        if index > 0:
            previous_frame = nodes_by_name.get(STORYBOARD_FRAME_NODES[index - 1])
            if previous_frame is not None and frame is not None:
                require_edge(
                    edge_keys,
                    str(previous_frame["id"]),
                    "image",
                    str(frame["id"]),
                    "reference_images",
                    1,
                    errors,
                )
        lines.append(f"storyboard frame {index + 1}: {frame_name}")

    for index, segment_name in enumerate(STORYBOARD_SEGMENT_NODES):
        segment = nodes_by_name.get(segment_name)
        frame = nodes_by_name.get(STORYBOARD_FRAME_NODES[index])
        allowed_app_node_types = {"veo-3.1"}
        if require_seamless_transition_keyframes and index < 3:
            allowed_app_node_types.add("veo-3.1-keyframes")
        validate_veo_node(
            segment,
            segment_name,
            expected_route="i2v",
            errors=errors,
            allowed_app_node_types=allowed_app_node_types,
            expected_resolution="1080p" if require_1080p_video else None,
        )
        require_parser_edge(parser, segment, index + 5, "text_prompt", edge_keys, errors)
        if frame is not None and segment is not None and not require_photo_enhancer_chains:
            require_any_edge_input(
                edges,
                str(frame["id"]),
                "image",
                str(segment["id"]),
                VIDEO_IMAGE_INPUT_CANDIDATES,
                errors,
            )
        lines.append(f"storyboard veo segment {index + 1}: {segment_name}")

    if require_photo_enhancer_chains:
        enhancer_lines, enhancer_errors = validate_photo_enhancer_chains(
            nodes_by_name, edges, edge_keys
        )
        lines.extend(enhancer_lines)
        errors.extend(enhancer_errors)
        if require_seamless_transition_keyframes:
            transition_lines, transition_errors = validate_seamless_transition_keyframes(
                nodes_by_name, edge_keys
            )
            lines.extend(transition_lines)
            errors.extend(transition_errors)

    preview_node = nodes_by_name.get("TCS Final: Veo 3.1 native audio video")
    final_node = nodes_by_name.get(final_name)
    if preview_node is not None:
        errors.append("Storyboard-to-Short should remove the old paid preview video node.")
    if preview_node is not None and final_node is not None:
        preview_edges = [
            edge
            for edge in edges
            if edge.get("from", {}).get("nodeId") == str(preview_node["id"])
            and edge.get("to", {}).get("nodeId") == str(final_node["id"])
        ]
        if preview_edges:
            errors.append(
                "Storyboard-to-Short final output must not stitch the director preview branch."
            )
    validate_single_exposed_generated_output(
        nodes_by_name.values(), "final_storyboard_short_16s", errors
    )
    lines.append("final output: final_storyboard_short_16s")
    return lines, errors


def validate_photo_enhancer_chains(
    nodes_by_name: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
    edge_keys: set[tuple[Any, ...]],
) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    errors: list[str] = []
    validator_name = PHOTO_ENHANCER_SHARED_NODES["validator"]
    question_name = PHOTO_ENHANCER_SHARED_NODES["question"]
    extractor_name = PHOTO_ENHANCER_SHARED_NODES["extractor"]

    for shared_name in PHOTO_ENHANCER_SHARED_NODES.values():
        if shared_name not in nodes_by_name:
            errors.append(f"Missing node: {shared_name}")

    for index, frame_name in enumerate(STORYBOARD_FRAME_NODES):
        segment_name = STORYBOARD_SEGMENT_NODES[index]
        step_names = photo_enhancer_step_names(index)
        frame = nodes_by_name.get(frame_name)
        segment = nodes_by_name.get(segment_name)
        analysis_1 = nodes_by_name.get(step_names["analysis_1"])
        prompt_1 = nodes_by_name.get(step_names["prompt_1"])
        first_pass = nodes_by_name.get(step_names["first_pass"])
        analysis_2 = nodes_by_name.get(step_names["analysis_2"])
        prompt_2 = nodes_by_name.get(step_names["prompt_2"])
        final_image = nodes_by_name.get(step_names["final_image"])

        validate_named_node(analysis_1, step_names["analysis_1"], "gemini", errors)
        validate_named_node(prompt_1, step_names["prompt_1"], "gemini", errors)
        validate_named_node(first_pass, step_names["first_pass"], "gemini-image-3-pro", errors)
        validate_gemini_image_node(
            first_pass, step_names["first_pass"], errors, expected_image_size="2K"
        )
        validate_named_node(analysis_2, step_names["analysis_2"], "gemini", errors)
        validate_named_node(prompt_2, step_names["prompt_2"], "gemini", errors)
        validate_named_node(final_image, step_names["final_image"], "gemini-image-3-pro", errors)
        validate_gemini_image_node(
            final_image, step_names["final_image"], errors, expected_image_size="2K"
        )

        require_named_edge(
            edge_keys,
            nodes_by_name,
            validator_name,
            "prompt",
            step_names["analysis_1"],
            "system_prompt",
            None,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            question_name,
            "prompt",
            step_names["analysis_1"],
            "prompt",
            None,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            frame_name,
            "image",
            step_names["analysis_1"],
            "images",
            0,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            step_names["analysis_1"],
            "text",
            step_names["prompt_1"],
            "prompt",
            None,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            extractor_name,
            "prompt",
            step_names["prompt_1"],
            "system_prompt",
            None,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            step_names["prompt_1"],
            "text",
            step_names["first_pass"],
            "text_prompt",
            None,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            frame_name,
            "image",
            step_names["first_pass"],
            "reference_images",
            0,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            step_names["first_pass"],
            "image",
            step_names["analysis_2"],
            "images",
            0,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            validator_name,
            "prompt",
            step_names["analysis_2"],
            "system_prompt",
            None,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            question_name,
            "prompt",
            step_names["analysis_2"],
            "prompt",
            None,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            step_names["analysis_2"],
            "text",
            step_names["prompt_2"],
            "prompt",
            None,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            extractor_name,
            "prompt",
            step_names["prompt_2"],
            "system_prompt",
            None,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            step_names["prompt_2"],
            "text",
            step_names["final_image"],
            "text_prompt",
            None,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            step_names["first_pass"],
            "image",
            step_names["final_image"],
            "reference_images",
            0,
            errors,
        )
        require_named_edge(
            edge_keys,
            nodes_by_name,
            step_names["final_image"],
            "image",
            segment_name,
            "startFrame",
            None,
            errors,
        )

        if frame is not None and segment is not None:
            reject_direct_storyboard_frame_to_segment_edge(edges, frame, segment, errors)
        lines.append(
            f"photo enhancer chain {index + 1}: {frame_name} -> {step_names['final_image']}"
        )
    return lines, errors


def validate_seamless_transition_keyframes(
    nodes_by_name: dict[str, dict[str, Any]],
    edge_keys: set[tuple[Any, ...]],
) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    errors: list[str] = []

    system_node = nodes_by_name.get("TCS Storyboard Director: system_prompt")
    if system_node is None:
        errors.append("Missing node: TCS Storyboard Director: system_prompt")
    else:
        system_prompt = system_node.get("nodeOutputs", {}).get("prompt", {}).get("value", "")
        if "Story-panel continuity upgrade" not in system_prompt:
            errors.append("Storyboard system prompt should include story-panel continuity guidance.")
        if "Seamless Transitions" not in system_prompt:
            errors.append("Storyboard system prompt should include seamless transition guidance.")

    for index in range(3):
        segment_name = STORYBOARD_SEGMENT_NODES[index]
        next_frame_name = photo_enhancer_step_names(index + 1)["final_image"]
        segment = nodes_by_name.get(segment_name)
        if segment is not None:
            inputs = segment.get("nodeInputs", {})
            if inputs.get("name", {}).get("value") != "workflow-veo3-1-keyframes-task":
                errors.append(f"{segment_name} should use workflow-veo3-1-keyframes-task.")
            if inputs.get("endFrame", {}).get("type") != "image":
                errors.append(f"{segment_name} should expose image input endFrame.")
        require_named_edge(
            edge_keys,
            nodes_by_name,
            next_frame_name,
            "image",
            segment_name,
            "endFrame",
            None,
            errors,
        )
        lines.append(
            f"seamless transition {index + 1}: {segment_name} lands on {next_frame_name}"
        )

    final_segment_name = STORYBOARD_SEGMENT_NODES[-1]
    final_segment = nodes_by_name.get(final_segment_name)
    if final_segment is not None:
        inputs = final_segment.get("nodeInputs", {})
        if inputs.get("name", {}).get("value") != "workflow-veo3-1-task":
            errors.append(f"{final_segment_name} should keep the proven standard Veo task.")
        if "endFrame" in inputs:
            errors.append(f"{final_segment_name} should not require a downstream endFrame.")

    return lines, errors


def photo_enhancer_step_names(index: int) -> dict[str, str]:
    prefix = f"TCS Photo Enhance {index + 1:02d}"
    return {key: f"{prefix}: {suffix}" for key, suffix in PHOTO_ENHANCER_STEP_SUFFIXES.items()}


def reject_direct_storyboard_frame_to_segment_edge(
    edges: list[dict[str, Any]],
    frame: dict[str, Any],
    segment: dict[str, Any],
    errors: list[str],
) -> None:
    frame_id = str(frame["id"])
    segment_id = str(segment["id"])
    for edge in edges:
        if (
            edge.get("from", {}).get("nodeId") == frame_id
            and edge.get("from", {}).get("nodeOutput") == "image"
            and edge.get("to", {}).get("nodeId") == segment_id
            and edge.get("to", {}).get("nodeInput") in VIDEO_IMAGE_INPUT_CANDIDATES
        ):
            errors.append(
                "Photo-enhanced storyboard should route through enhancer output before Veo: "
                f"{node_name(frame)}.image -> {node_name(segment)}.{edge['to']['nodeInput']}"
            )


def validate_gemini_image_node(
    node: dict[str, Any] | None,
    node_name_for_error: str,
    errors: list[str],
    *,
    expected_image_size: str = "1K",
) -> None:
    inputs = node.get("nodeInputs", {})
    if inputs.get("model", {}).get("value") != "gemini-3-pro-image-preview":
        errors.append(f"{node_name_for_error} should use gemini-3-pro-image-preview.")
    if inputs.get("image_size", {}).get("value") != expected_image_size:
        errors.append(f"{node_name_for_error} should use {expected_image_size} image_size.")
    if inputs.get("aspect_ratio", {}).get("value") != "9:16":
        errors.append(f"{node_name_for_error} should use 9:16 aspect_ratio.")


def validate_veo_node(
    node: dict[str, Any] | None,
    node_name_for_error: str,
    *,
    expected_route: str,
    errors: list[str],
    allowed_app_node_types: set[str] | None = None,
    expected_resolution: str | None = None,
) -> None:
    if node is None:
        errors.append(f"Missing node: {node_name_for_error}")
        return

    expected_app_node_types = allowed_app_node_types or {"veo-3.1"}
    if node.get("appNodeType") not in expected_app_node_types:
        expected_types = ", ".join(sorted(expected_app_node_types))
        errors.append(
            f"{node_name_for_error} has appNodeType {node.get('appNodeType')!r}; "
            f"expected one of: {expected_types}."
        )
    if node is None:
        return
    inputs = node.get("nodeInputs", {})
    if inputs.get("route", {}).get("value") != expected_route:
        errors.append(f"{node_name_for_error} route should be {expected_route!r}.")
    if inputs.get("noAudio", {}).get("value") is not False:
        errors.append(f"{node_name_for_error} should keep native audio enabled.")
    if inputs.get("seconds", {}).get("value") != 4:
        errors.append(f"{node_name_for_error} should use 4 seconds in the Workflow canvas.")
    if inputs.get("aspectRatio", {}).get("value") != "9:16":
        errors.append(f"{node_name_for_error} should use 9:16 aspectRatio.")
    if expected_resolution and inputs.get("resolution", {}).get("value") != expected_resolution:
        errors.append(f"{node_name_for_error} should use {expected_resolution} resolution.")


def validate_parser_paths(
    node: dict[str, Any] | None,
    node_name_for_error: str,
    expected_paths: list[str],
    errors: list[str],
) -> None:
    if node is None:
        return
    actual_paths = [
        path.get("path")
        for path in node.get("nodeInputs", {}).get("paths", {}).get("value", [])
        if isinstance(path, dict)
    ]
    missing_paths = [path for path in expected_paths if path not in actual_paths]
    if missing_paths:
        errors.append(f"{node_name_for_error} is missing parser paths: {', '.join(missing_paths)}")


def require_parser_edge(
    parser: dict[str, Any] | None,
    target: dict[str, Any] | None,
    parser_index: int,
    target_input: str,
    edge_keys: set[tuple[Any, ...]],
    errors: list[str],
    *,
    target_index: int | None = None,
) -> None:
    if parser is None or target is None:
        return
    require_edge(
        edge_keys,
        str(parser["id"]),
        "text",
        str(target["id"]),
        target_input,
        target_index,
        errors,
        source_index=parser_index,
    )


def validate_single_exposed_generated_output(
    nodes: Any, expected_label: str, errors: list[str]
) -> None:
    exposed_generated_outputs: list[tuple[str, str]] = []
    for node in nodes:
        if node_name(node).startswith("TCS Input:"):
            continue
        for output_key, output in node.get("nodeOutputs", {}).items():
            if output.get("exposedToApp") is True:
                exposed_generated_outputs.append(
                    (node_name(node), str(output.get("label") or output_key))
                )
    if len(exposed_generated_outputs) != 1:
        errors.append(
            "Expected exactly one exposed generated output; found "
            + ", ".join(f"{name}:{label}" for name, label in exposed_generated_outputs)
        )
        return
    _, actual_label = exposed_generated_outputs[0]
    if actual_label != expected_label:
        errors.append(
            f"Exposed generated output label is {actual_label!r}; expected {expected_label!r}."
        )


def validate_named_node(
    node: dict[str, Any] | None,
    node_name_for_error: str,
    app_node_type: str,
    errors: list[str],
) -> None:
    if node is None:
        errors.append(f"Missing node: {node_name_for_error}")
        return
    if node.get("appNodeType") != app_node_type:
        errors.append(
            f"{node_name_for_error} has appNodeType {node.get('appNodeType')!r}; "
            f"expected {app_node_type!r}."
        )


def require_named_edge(
    edge_keys: set[tuple[Any, ...]],
    nodes_by_name: dict[str, dict[str, Any]],
    source_name: str,
    source_output: str,
    target_name: str,
    target_input: str,
    target_index: int | None,
    errors: list[str],
) -> None:
    source_node = nodes_by_name.get(source_name)
    target_node = nodes_by_name.get(target_name)
    if source_node is None:
        errors.append(f"Missing source node: {source_name}")
        return
    if target_node is None:
        errors.append(f"Missing target node: {target_name}")
        return
    require_edge(
        edge_keys,
        str(source_node["id"]),
        source_output,
        str(target_node["id"]),
        target_input,
        target_index,
        errors,
    )


def require_edge(
    edge_keys: set[tuple[Any, ...]],
    source_node_id: str,
    source_output: str,
    target_node_id: str,
    target_input: str,
    target_index: int | None,
    errors: list[str],
    *,
    source_index: int | None = None,
) -> None:
    edge_key = (
        source_node_id,
        source_output,
        source_index,
        target_node_id,
        target_input,
        target_index,
    )
    if edge_key not in edge_keys:
        source_suffix = "" if source_index is None else f"[{source_index}]"
        target_suffix = "" if target_index is None else f"[{target_index}]"
        errors.append(
            "Missing edge: "
            f"{source_node_id}.{source_output}{source_suffix} -> "
            f"{target_node_id}.{target_input}{target_suffix}"
        )


def require_any_edge_input(
    edges: list[dict[str, Any]],
    source_node_id: str,
    source_output: str,
    target_node_id: str,
    target_inputs: set[str],
    errors: list[str],
) -> None:
    for edge in edges:
        if (
            edge.get("from", {}).get("nodeId") == source_node_id
            and edge.get("from", {}).get("nodeOutput") == source_output
            and edge.get("to", {}).get("nodeId") == target_node_id
            and edge.get("to", {}).get("nodeInput") in target_inputs
        ):
            return
    errors.append(
        "Missing image-to-video reference edge: "
        f"{source_node_id}.{source_output} -> {target_node_id}."
        f"one_of({', '.join(sorted(target_inputs))})"
    )


def build_edge_keys(edges: list[dict[str, Any]]) -> set[tuple[Any, ...]]:
    return {
        (
            edge.get("from", {}).get("nodeId"),
            edge.get("from", {}).get("nodeOutput"),
            edge.get("from", {}).get("index"),
            edge.get("to", {}).get("nodeId"),
            edge.get("to", {}).get("nodeInput"),
            edge.get("to", {}).get("index"),
        )
        for edge in edges
    }


def index_nodes_by_name(
    nodes: list[dict[str, Any]], errors: list[str]
) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        grouped[node_name(node)].append(node)

    indexed: dict[str, dict[str, Any]] = {}
    for name, named_nodes in grouped.items():
        if len(named_nodes) > 1:
            errors.append(f"Duplicate graph node name: {name}")
        indexed[name] = named_nodes[0]
    return indexed


def node_name(node: dict[str, Any]) -> str:
    return str(node.get("nodeProps", {}).get("name", ""))


def print_report(
    workflow_id: str,
    input_lines: list[str],
    mode_lines: list[str],
    warnings: list[str],
    errors: list[str],
) -> None:
    print("Runway workflow contract check")
    print(f"workflow_id: {workflow_id or '(not configured)'}")
    if input_lines:
        print("\nInputs")
        for line in input_lines:
            print(f"- {line}")
    if mode_lines:
        print("\nGraph Mode")
        for line in mode_lines:
            print(f"- {line}")
    if warnings:
        print("\nWarnings")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("\nErrors")
        for error in errors:
            print(f"- {error}")
        return
    if mode_lines:
        print("\nResult: workflow mapping, director chain, and graph mode verified.")
    else:
        print("\nResult: workflow mapping and director chain verified.")


if __name__ == "__main__":
    raise SystemExit(main())
