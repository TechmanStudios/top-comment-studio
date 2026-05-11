# Runway Workflow Build Guide

Use this guide to build and publish the Top Comment Studio Runway workflow. Historical Seedance checkpoints are preserved below for diagnostics, but the current hackathon workflow should use Gen-4.5 and Veo 3.1.

## Workflow

Name: `TCS Gen/Veo Director v2`

Primary output: one polished vertical YouTube Short video with sound.

Core method:

```text
approved top-comment package
  -> unified Gen/Veo audio-video director packet
  -> nine generated Nano Banana image references
  -> optional Gen-4.5 silent cinematic shot studies
  -> final Veo 3.1 audio-native video
```

## Current Gen/Veo Pivot

Do not preserve the old Seedance-oriented TCS13 method as the active creative contract. Use a unified Gen/Veo audio-video director packet instead: audience signal, creator intent, subject continuity, scene world, visual anchor, motion arc, camera language, audio design, audio-video sync, negative constraints, duration, aspect, and safety. Nano Banana Pro / Gemini 3 Pro Image still makes the nine-image board in this order: hook frame, hero subject, setting/world, palette/mood, material/texture, action pose, transition/twist, payoff/reveal, thumbnail final beat.

This mimics the useful part of Seedance 2's unified multimodal direction at the orchestration layer: the app plans audio and video together before model submission. It does not claim access to Seedance's internal joint architecture. Gen-4.5 receives the visual/motion subset for silent shot studies; Veo 3.1 receives the full packet so native audio cues are locked to visible causes.

Public Runway API constraints from the current docs:

- `POST /v1/image_to_video` supports `gen4.5` and `veo3.1`, but accepts one `promptImage` only.
- `POST /v1/text_to_video` supports `gen4.5` and `veo3.1`, but is prompt-only in the public docs.
- Vertical video ratio is `720:1280`, duration is 2-10 seconds.
- No public Precision v2 / Magnific upscaler endpoint or model slug has been confirmed.

Runway Workflow canvas checkpoint note: the published Workflow Veo 3.1 node rejected `seconds=10` with `Invalid task options: seconds: Invalid input` on endpoint `fb490b2c-aa0e-4e31-95eb-12b88c7bc6fc`. The working grouped Workflow checkpoint should use `seconds=4`, `aspectRatio=9:16`, and `noAudio=false` until another canvas-supported duration is proven. The direct public API lane can keep its own documented duration settings.

## Programmatic Workflow Build Playbook

This section captures the reusable process for building future Runway workflow structures from code or browser-assisted graph mutation. The short version: mutate the canvas graph, validate it internally, save a new canvas version, publish that version, retrieve the published Developer API graph, then verify and smoke that exact endpoint.

Runway has two API surfaces:

1. Canvas/editor surface: `https://api.runwayml.com/v1/dynamic_workflows/...`. This is what the Runway web app uses for graph versions, validation, featured workflows, and Developer Portal publishing. It requires the current browser session auth and workspace header. Never save or print those secret values.
2. Developer API surface: `https://api.dev.runwayml.com`. This is what Top Comment Studio should call at runtime using `Authorization: Bearer <RUNWAYML_HACKATHON_API_SECRET>` and `X-Runway-Version: 2024-11-06`.

The useful internal calls observed during this build:

```text
GET  /v1/dynamic_workflows/{canvas_workflow_id}/versions/latest
POST /v1/dynamic_workflows/validate
POST /v1/dynamic_workflows/{canvas_workflow_id}/versions
POST /v1/dynamic_workflows_devportal_published
GET  /v1/dynamic_workflows_featured/{featured_workflow_id}
```

The useful Developer API calls:

```text
GET  /v1/workflows/{published_endpoint_id}
POST /v1/workflows/{published_endpoint_id}
GET  /v1/workflow_invocations/{invocation_id}
```

Canvas workflow IDs and published endpoint IDs are different. For the current graph, `ba325b07-a845-4fe6-901e-9242666ef8c7` is the editor canvas ID, while `c1b49d17-c80f-4705-b0e6-86c89a070464` is the published Developer API endpoint ID. A Developer API 404 usually means those IDs were mixed up.

### Save, Publish, Verify Loop

Use this loop for every new structure:

1. Fetch the latest canvas version and clone its graph in memory.
2. Make the smallest useful mutation: one model stage, one routing fix, one output exposure change, or one layout cleanup.
3. Preserve existing TCS input node IDs and names unless replacement is unavoidable.
4. Run internal `/dynamic_workflows/validate` on the full graph.
5. Save a new canvas version with the latest server `version` number.
6. Publish the saved canvas version to the Developer Portal.
7. Retrieve the published endpoint graph through `api.dev.runwayml.com`.
8. Run the local verifier against the published endpoint.
9. Run one paid smoke only after static verification passes.
10. Probe the downloaded MP4 with `ffprobe` and save a contact sheet when visual continuity matters.

Do not trust any one layer alone. The version 65 checkpoint saved a valid-looking 1080p canvas graph but published a Developer API endpoint with empty TCS input labels and no exposed final output. Version 66 restored the published input/output metadata and is the usable checkpoint.

### Graph Anatomy Rules

For app-controlled values, use primitive Text input nodes named `TCS Input: <logical_name>`. Expose their `prompt` output and keep the output label aligned with the logical name. Give every input a distinct default value so manual editor runs and published endpoint inspection stay readable.

Use stable, searchable names for generated stages. The verifier and future scripts depend on names like:

```text
TCS Director: Claude Veo prompt
TCS Asset Planner: board/sidecar/segments JSON
TCS Continuity Core: enriched creative brief
TCS Storyboard Frame 01: hook
TCS Photo Enhance 01: final enhanced frame
TCS Storyboard Segment 01: hook native audio
TCS Storyboard Final: stitched 16s short
```

For Text/Combine nodes created in graph JSON, include both:

```json
{
  "subTaskType": "concat",
  "nodeInputs": {
    "subTaskType": {"type": "primitive", "value": "concat"}
  }
}
```

The internal validator accepted Combine nodes without the top-level `subTaskType`, but the editor UI did not render them correctly. Prefer a serial Combine chain over a wide fan-in; the parallel Combine checkpoint produced `Node is already running in this execution` errors.

For JSON parser fanout, follow Runway's example pattern: parser output key stays `text`, and each edge chooses a parsed path with `from.index`. Do not feed downstream prompts from invented output names such as `text[0]`. If a model node expects a scalar prompt, route parser output through a concat/text normalizer before the model node.

For generated images into Veo Workflow nodes, use scalar frame fields:

- Normal image-to-video: image output -> `startFrame`.
- Seamless adjacent transition: current image output -> `startFrame`; next image output -> `endFrame`.
- Do not use indexed `promptImage[0]` inside Workflow Veo nodes. That statically verified in version 55 but failed at paid runtime because `startFrame` was undefined.

Delete disconnected or abandoned model nodes before publishing. Published workflow invocations can still schedule disconnected branches, which creates cost and failure risk even if the final output path looks clean.

### Model Node Type Crib Sheet

Published Workflow runtime checks care about `appNodeType`, not only the visible model label. These are the values proven or rejected in this repo:

| Purpose | Workflow task type | Runtime-safe `appNodeType` | Proven settings and notes |
|---|---|---|---|
| Gemini Image Pro / Nano Banana Pro | `workflow_gemini_image` | `gemini-image-3-pro` | Use model value `gemini-3-pro-image-preview`; copied image nodes without app node types fail publish. |
| Gemini API text/vision analysis | `workflow_gemini_api` | `gemini` | `gemini-api` passed static checks but failed paid runtime with `Invalid app node type`. |
| Gen-4.5 image-to-video | `workflow_gen4_5` | `gen4_5-image-to-video` | Use for silent shot studies or motion previsuals. |
| Veo 3.1 standard video | `workflow_veo3_1` | `veo-3.1` | Proven with `seconds=4`, `aspectRatio=9:16`, `noAudio=false`, `resolution=720p` and `1080p`. |
| Veo 3.1 keyframe video | `workflow_veo3_1` | `veo-3.1-keyframes` | Proven for first three v66 segments with scalar `startFrame` + `endFrame`. |
| Stitch Videos | `workflow_media_processing_v2` | `stitch-video` | Uses input key `input` and output key `video`. |
| GPT Image 2 in current Workflow publish path | varies | `gpt-tidepool-alpha` | Avoid for published workflow demos; paid invocations hit `No model variant mapping`. |

Resolution and aspect lessons:

- Workflow Veo uses `aspectRatio=9:16`; the app's logical Shorts aspect can remain `1080:1920`.
- `resolution=720p` produces 720x1280 vertical MP4s.
- `resolution=1080p` validated and paid-smoked in version 66, producing true 1080x1920 H.264 + AAC output.
- Keep Workflow Veo segment duration at `seconds=4` until another duration is proven in the canvas runtime.

### Featured Workflow Harvesting

Featured workflows are best used as pattern references. Do not paste a large graph into TCS without reducing it to the smallest compatible proof first.

Useful examples already inspected:

- Featured workflow `661`, Storyboard to Film: continuity spine with one storyboard JSON, identity/world anchor, sequential frames, per-shot motion, and final assembly.
- Featured workflow `596`, Photo Enhancer: two-pass Gemini analysis and prompt refinement before generating an enhanced frame.
- Featured workflow `529`, Story Panels: continuity language for panel-to-panel consistency and one evolving scene.
- Featured workflow `364`, Seamless Transitions: adjacent keyframe routing where a video starts on one image and lands on the next.

When harvesting a featured workflow, inspect the graph fields that matter at runtime: task type, `appNodeType`, `nodeInputs`, `nodeOutputs`, exposed outputs, edge `from.index`, edge `to.index`, and frame input names. Rebuild the TCS version one stage at a time and publish a checkpoint before combining patterns.

### Validation Ladder

Use increasingly expensive checks:

1. Internal graph validation: catches malformed graph structure before saving.
2. Published graph retrieval: confirms the Developer API sees the same node names, labels, inputs, outputs, and app node types.
3. Local verifier: confirms the TCS contract and expected graph mode.
4. Paid smoke: proves runtime model handoffs, output exposure, audio/video output, and node-error behavior.
5. Local artifact inspection: `ffprobe`, contact sheet, and local playback for resolution, audio, and continuity.

Current v66 verifier command:

```powershell
uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains --require-seamless-transition-keyframes --require-1080p-video
```

Paid smoke command shape:

```powershell
uv run python scripts/run_runway_workflow_smoke.py <published_endpoint_id> --output-dir data/local/runway_outputs --poll-seconds 30 --max-polls 90
```

Treat `SUCCEEDED` with empty output as a failure until proven otherwise. Inspect `nodeErrors`, output exposure, and model handoff fields. If needed, reproduce with raw curl to rule out local client shape problems.

Current paid-proven 1080p seamless-keyframe Gen/Veo Continuity Core checkpoint: canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`, endpoint `c1b49d17-c80f-4705-b0e6-86c89a070464`, published version 66. It keeps the version 63 seamless-keyframe continuity design, spaces the Photo Enhancer and Veo rows for cleaner editor inspection, and sets all four Veo 3.1 segment nodes to `resolution=1080p`. Enhanced frame 02 feeds segment 01 `endFrame`, enhanced frame 03 feeds segment 02 `endFrame`, and enhanced frame 04 feeds segment 03 `endFrame`, while all four enhanced frames still feed their matching segment `startFrame`. The first three Veo 3.1 nodes use `appNodeType: veo-3.1-keyframes` and `workflow-veo3-1-keyframes-task`; the final payoff segment stays on the proven standard `appNodeType: veo-3.1` and `workflow-veo3-1-task`. The graph has 68 nodes, 131 edges, 10 exposed TCS inputs, and the same generated output label: `final_storyboard_short_16s`. Internal Runway validation passed, Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains --require-seamless-transition-keyframes --require-1080p-video`, and paid smoke invocation `f805c55d-4ed3-461a-ac82-1153c828904b` completed `SUCCEEDED` with one MP4 and empty node errors. Local artifact `data/local/runway_outputs/f805c55d-4ed3-461a-ac82-1153c828904b_6e092b87-1cef-4b69-8a78-3a62fb08869f_item_1.mp4` probes as H.264 video at 1080x1920 plus AAC audio, about 16 seconds. Contact sheet: `data/local/runway_outputs/f805c55d-4ed3-461a-ac82-1153c828904b_contact_sheet.jpg`; safe result note: `data/local/runway_outputs/f805c55d-4ed3-461a-ac82-1153c828904b_result.json`.

Do not use intermediate endpoint `c5882933-e837-432d-b59e-d255be020d29` from version 65. It saved the 1080p/layout graph, but the published Developer API endpoint dropped input labels and the exposed final output; version 66 fixed those publish fields.

Previous paid-proven 720p seamless-keyframe Gen/Veo Continuity Core checkpoint: canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`, endpoint `65e09485-4169-41d9-9282-85b52148949f`, published version 63. It keeps the version 62 photo-enhanced Continuity Core, adds Story Panels-inspired continuity instructions from featured workflow `529`, and borrows the Seamless Transitions keyframe pattern from featured workflow `364`: enhanced frame 02 feeds segment 01 `endFrame`, enhanced frame 03 feeds segment 02 `endFrame`, and enhanced frame 04 feeds segment 03 `endFrame`, while all four enhanced frames still feed their matching segment `startFrame`. The graph has 68 nodes, 131 edges, 10 exposed TCS inputs, and the same generated output label: `final_storyboard_short_16s`. Paid smoke invocation `f6522ddd-ec5c-486f-80a3-a50906993ea8` completed `SUCCEEDED` with one 720x1280 MP4 and empty node errors.

Previous paid-proven photo-enhanced Gen/Veo Continuity Core checkpoint: canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`, endpoint `277aecec-43a4-4042-844e-e9e3d41db8d3`, published version 62. It keeps the version 59 Continuity Core spine, inserts the Runway featured workflow `596` Photo Enhancer method between each Gemini storyboard frame and its downstream Veo 3.1 segment, and routes only the final enhanced frame into the segment's scalar `startFrame`. The graph has 68 nodes, 128 edges, 10 exposed TCS inputs, and the same generated output label: `final_storyboard_short_16s`. Internal Runway validation passed, Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains`, and paid smoke invocation `cc30e6ea-f938-45b7-8d56-8ac62c314c67` completed `SUCCEEDED` with one MP4 and no node errors. Local artifact `data/local/runway_outputs/cc30e6ea-f938-45b7-8d56-8ac62c314c67_6e092b87-1cef-4b69-8a78-3a62fb08869f_item_1.mp4` probes as H.264 video plus AAC audio, about 16 seconds. Contact sheet: `data/local/runway_outputs/cc30e6ea-f938-45b7-8d56-8ac62c314c67_contact_sheet.jpg`; safe result note: `data/local/runway_outputs/cc30e6ea-f938-45b7-8d56-8ac62c314c67_result.json`.

Previous paid-proven Gen/Veo Continuity Core baseline: canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`, endpoint `31f64606-73bf-4b43-ba53-596e92fc26bd`, published version 59. It preserves the paid-proven Storyboard-to-Short spine and makes the outer TCS Director and TCS Asset Planner part of the creative process before generation: raw 10-field brief -> TCS Director Claude treatment + TCS Asset Planner JSON -> `TCS Asset Parser: boards sidecars segments` -> `TCS Asset Planner: parsed creative map` -> `TCS Continuity Core: enriched creative brief` -> storyboard continuity JSON -> anchor/frame/segment/final stitch. The graph has 41 nodes, 72 edges, 10 exposed TCS inputs, and one generated output label: `final_storyboard_short_16s`. Internal Runway validation passed before save/publish, static Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core`, and paid smoke invocation `cc086bdd-3a14-4290-a6e8-bbb7c7f10788` completed `SUCCEEDED` with one MP4 and no node errors. Local artifact `data/local/runway_outputs/cc086bdd-3a14-4290-a6e8-bbb7c7f10788_6e092b87-1cef-4b69-8a78-3a62fb08869f_item_1.mp4` probes as H.264 video plus AAC audio, about 16 seconds. Contact sheet: `data/local/runway_outputs/cc086bdd-3a14-4290-a6e8-bbb7c7f10788_contact_sheet.jpg`; safe result note: `data/local/runway_outputs/cc086bdd-3a14-4290-a6e8-bbb7c7f10788_result.json`.

Previous paid-proven Gen/Veo Continuity Core checkpoint: endpoint `dbe78d91-05ca-460d-a71f-568164577793`, published version 57. Paid smoke invocation `e0b2d638-7276-41d8-ad29-6d166e80fd96` completed `SUCCEEDED` with one MP4 and no node errors; local artifact `data/local/runway_outputs/e0b2d638-7276-41d8-ad29-6d166e80fd96_final_storyboard_short_16s.mp4` probes as H.264 video plus AAC audio, about 16 seconds. Contact sheet: `data/local/runway_outputs/e0b2d638-7276-41d8-ad29-6d166e80fd96_contact_sheet.jpg`.

1080p seamless-keyframe paid-smoke creative read: version 66 is the strongest continuity result so far. The storm-powered floating structure stays centered and recognizable from hook to payoff, the keyframe `endFrame` routing makes adjacent segments land on the next enhanced panel instead of restarting from unrelated imagery, and the color arc moves cleanly from charged storm blues into a warm golden payoff. Version 63 remains the paid-proven 720p fallback if 1080p cost or latency becomes a rehearsal issue.

Previous published Gen/Veo Storyboard-to-Short checkpoint: canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`, endpoint `4af4b372-b117-49bd-9a7e-4812430f76eb`, published version 56. It preserves the 10 app inputs, runs them through one storyboard director JSON node, generates one identity/world anchor, four sequential Nano Banana Pro storyboard frames, four Veo 3.1 image-to-video segments, and one final Stitch Videos output. The public API contract exposes one generated output only: `final_storyboard_short_16s`. Static Developer API verification with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-storyboard-to-short` passed. Paid smoke invocation `4b700e61-d835-433b-b330-5f58f2cefa8f` completed `SUCCEEDED` with one MP4 and no node errors; local artifact `data/local/runway_outputs/4b700e61-d835-433b-b330-5f58f2cefa8f_final_storyboard_short_16s.mp4` probes as H.264 video plus AAC audio, about 16 seconds. Contact sheet: `data/local/runway_outputs/4b700e61-d835-433b-b330-5f58f2cefa8f_contact_sheet.jpg`.

Storyboard-to-Short schema lesson: endpoint `1766f759-d1ec-4cce-9a82-7386e8a72983`, published version 55, statically verified but failed the paid smoke at runtime. Invocation `b994efd0-6c3a-427d-a539-7ffe87c384d3` reported Veo segment node errors like `Invalid task options: startFrame: Invalid input: expected object, received undefined` while the graph still showed `RUNNING`. The fix was to wire each storyboard frame to the Veo 3.1 segment node's scalar `startFrame` input, not indexed `promptImage[0]`. Static Runway validation accepts multiple image-input spellings, so paid smoke remains the source of truth for Workflow Veo I2V routing.

Previous published Gen/Veo final-master checkpoint: canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`, endpoint `26bf091b-6f75-49c4-bd74-4de137eef9ce`, published version 54. It preserves the 10 app inputs, the proven director/Veo 4-second preview lane, and the asset-planner branch, then adds one final Stitch Videos node that combines the director preview with the 16-second asset-planner final. The public API contract exposes one generated output only: `final_final_video_20s`. Static Developer API verification confirmed 48 nodes, 54 edges, 10 exposed TCS inputs, 1 exposed generated output, and no missing workflow `appNodeType` values. Paid smoke invocation `ce9d109c-8a3b-4fcf-9ae3-0ad1ecf6d16d` completed `SUCCEEDED` with one MP4, no node errors; local artifact `data/local/runway_outputs/ce9d109c-8a3b-4fcf-9ae3-0ad1ecf6d16d_final_final_video_20s.mp4` probes as H.264 video plus AAC audio, about 20 seconds.

Continuity lesson from the paid smoke: the endpoint works technically, but stitching the 4-second director preview to the independently planned 16-second asset branch behaves like a reel of related shots rather than one coherent short. The contact sheet shows the floating-city subject changes forms across the stitched sections. Do not deepen this branch-stitch design as the final creative path.

Previous exposed-assets Gen/Veo checkpoint: canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`, endpoint `c38549da-a2b8-4541-96a0-db14af640184`, published version 52. It exposed the 4-second preview, all 9 board panels, all 3 sidecar shots, and `long_final_video_16s` for inspection. Keep it as the debugging/visual-QA checkpoint when Bryan wants to inspect the intermediate assets.

Previous proven Gen/Veo director-stage checkpoint: canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`, endpoint `9ed1d223-c002-4f4d-b750-c43f0f3de8d8`, published version 41. It keeps the 10 app inputs exposed, runs them through a 9-node serial Combine Text chain, feeds one hidden Claude director prompt, and sends the resulting compact prompt into Veo 3.1. Paid test invocation `201a6753-3100-4b01-92fb-14698be41309` completed `SUCCEEDED`, returned one MP4, and `ffprobe` confirmed H.264 video plus AAC audio.

Adapter policy:

1. Pick Gen-4.5 for the best silent cinematic shots and motion studies.
2. Pick Veo 3.1 for the final output because the final video needs sound/native audio.
3. When creating final video from the board, use one hero/upscaled board image as the API `promptImage` and encode the remaining board plan plus the AV director packet into the prompt.
4. Only run enhancement after Nano Banana Pro images exist and before they are used as video references. The version 62 Workflow checkpoint uses featured workflow `596` Photo Enhancer chains for this in-graph; Precision v2 or another public upscaler API is still unconfirmed.

Ephemeral upload policy: use Runway ephemeral uploads for app-side second-stage runs when local files or downloaded outputs need stable `runway://` asset URIs. They are valid for 24 hours, accept files from 512 bytes to 200 MB, require purchased credits, and are rate limited. They do not combine assets by themselves and they do not avoid upstream Workflow generation cost; they only make assets usable anywhere the public API accepts a URL/data URI.

## Storyboard-to-Short Continuity Direction

Runway featured workflow `661` (`Storyboard to Film`) is the right pattern to adapt for the next Gen/Veo graph. Its useful structure is not the specific Kling model choice; it is the continuity spine:

1. One story/script input is transformed into a strict storyboard JSON object.
2. A character/identity sheet is generated first.
3. Rough storyboard frames are generated in sequence.
4. Polished frames reference the identity sheet, the rough frame, and prior polished frame(s).
5. Motion prompts are generated from each polished frame plus its storyboard text.
6. Video shots are generated from the polished frames, then assembled.

Adapt this as `Storyboard-to-Short` for TCS: the 10 app inputs should feed one storyboard architect that outputs a continuity bible plus 4-5 final beats, not two separate director/asset branches. Generate one hero identity/world anchor, then generate each board/hero frame with references to the anchor and the previous finalized frame. Feed those frames into Veo 3.1 image-to-video segment nodes when the Workflow canvas supports Veo image input; otherwise keep a public API second-stage lane that uploads/uses the frames as `runway://` or URL prompt images. Stitch only segments that came from the same storyboard spine.

Continuity Core checkpoint: version 59 wraps the proven Storyboard-to-Short graph with the outer creative planning ring and explicitly routes the parsed Asset Planner outputs into the Continuity Core. Shape: 41 nodes, 72 edges, 10 exposed TCS inputs, serial Combine chain, `TCS Director: system_prompt`, `TCS Director: Claude Veo prompt`, `TCS Asset Planner: system_prompt`, `TCS Asset Planner: board/sidecar/segments JSON`, `TCS Asset Parser: boards sidecars segments`, `TCS Asset Planner: parsed creative map`, `TCS Continuity Core: enriched creative brief`, then the existing storyboard continuity JSON, parser, anchor, four frames, four Veo 3.1 `i2v` segments using scalar `startFrame`, two intermediate stitch nodes, and one final stitch output labeled `final_storyboard_short_16s`. This keeps the prior director and asset-planner groupings as upstream text intelligence without reconnecting the old independent media branch. Paid smoke `cc086bdd-3a14-4290-a6e8-bbb7c7f10788` proved version 59 generates one 16-second native-audio MP4 with no node errors.

Photo-enhanced Continuity Core checkpoint: version 62 inserts the featured Photo Enhancer method after each storyboard frame and before Veo. Per beat: storyboard frame -> Gemini API analysis -> Gemini API prompt extraction -> 2K Gemini Image first pass -> second Gemini API analysis/prompt extraction -> 2K Gemini Image final enhanced frame -> Veo 3.1 `startFrame`. Shape: 68 nodes, 128 edges, same 10 exposed TCS inputs, same `final_storyboard_short_16s` output. Verify with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains`. Runtime lesson: version 61 endpoint `6e9bac23-016f-4f40-857e-d846132623ac` used `appNodeType: gemini-api` for the Gemini API analysis nodes and paid invocation `147f5d4f-bd19-454b-a223-2a1ba3d1f2e3` reported `Invalid app node type: gemini-api` with no MP4 output. Version 62 fixes those nodes to `appNodeType: gemini` and paid invocation `cc30e6ea-f938-45b7-8d56-8ac62c314c67` succeeded with one native-audio MP4.

1080p seamless-keyframe Continuity Core checkpoint: version 66 builds on version 63 by preserving story-panel continuity guidance and adjacent Veo keyframe transitions, setting all four Veo segments to `1080p`, and spacing the generated-frame/enhancer/video rows for editor inspection. The first three Veo 3.1 segments still start from their own enhanced frame, but also receive the next enhanced frame on scalar `endFrame`; the final payoff segment keeps only `startFrame`. Shape: 68 nodes, 131 edges, same 10 exposed TCS inputs, same `final_storyboard_short_16s` output. Verify with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains --require-seamless-transition-keyframes --require-1080p-video`. Paid invocation `f805c55d-4ed3-461a-ac82-1153c828904b` succeeded with one native-audio 1080x1920 MP4 and empty node errors.

Saved/published checkpoint: version 56 is the paid-proven Storyboard-to-Short graph. Shape: 34 nodes, 47 edges, 10 exposed TCS inputs, one `TCS Storyboard Director: continuity JSON` Claude node, one JSON parser, one `TCS Storyboard Anchor: identity/world reference`, four sequential Gemini Pro storyboard frames, four Veo 3.1 `i2v` segment nodes using scalar `startFrame`, two intermediate stitch nodes, and one final stitch output labeled `final_storyboard_short_16s`. The graph removed the old paid 4-second preview-video branch from the final path and exposes exactly one generated output.

Target node names for the next saved/published checkpoint:

```text
TCS Storyboard Director: system_prompt
TCS Storyboard Director: continuity JSON
TCS Storyboard Parser: continuity JSON
TCS Storyboard Anchor: identity/world reference
TCS Storyboard Frame 01: hook
TCS Storyboard Frame 02: escalation
TCS Storyboard Frame 03: transformation
TCS Storyboard Frame 04: payoff
TCS Storyboard Segment 01: hook native audio
TCS Storyboard Segment 02: escalation native audio
TCS Storyboard Segment 03: transformation native audio
TCS Storyboard Segment 04: payoff native audio
TCS Storyboard Final: stitched 16s short
```

After publishing that checkpoint, verify it before spending credits:

```powershell
uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-storyboard-to-short
```

For the Continuity Core checkpoint, verify the outer director/asset-planner ring plus the storyboard spine:

```powershell
uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core
```

The package page now follows this public-API-safe path: direct Nano Banana image -> Gen-4.5 cinematic shot, and nine-image board -> Veo 3.1 image-to-video final with native-audio prompt direction from the unified AV packet.

## Historical Seedance Diagnostics

## V1.1 Reference Clip Braid

The v1 workflow ships one final Seedance hero clip from the director prompt plus first/last image references. The v1.1 direction is to enrich that final clip by generating three short reference clips first.

Methodology: treat the final Seedance hero clip as the only finished product, and use the image and short-video assets as upstream reference material. The board has nine Nano Banana image references, grouped into three triptychs. Each triptych creates one short Seedance reference clip, with sound-design direction folded into the clip prompt while sidecar audio is disabled. The final Seedance hero clip then receives the refined Seedance prompt plus the three reference clips, instead of trying to feed only a couple of raw images into the final node.

Current image-board-first checkpoint: keep the reliable hero MP4 endpoint on `e4a221ab-743d-45ac-bc47-633d66227614`, generate the nine image references in a dedicated app lane through three proven row workflows, then create the next final MP4 with Seedance text-to-video image references. The direct Seedance docs path uses `POST /v1/text_to_video` with `references: [{"uri": image_url}]`, up to nine images, and task `5bf9b443-cdf0-443c-b752-9e292592e69b` completed `SUCCEEDED` with one MP4. Published workflow checkpoint `8ab20d96-444e-4751-aa91-9c0b44c5036c` mirrors that direction inside Workflows by routing all nine generated images into final Seedance `referenceImages`, with no `firstFrame`, `lastFrame`, or `referenceVideos` edges, but live invocation `f030c851-4eea-41ce-b3a3-7a5b3f86658d` finished `SUCCEEDED` with empty output. A later one-image diagnostic endpoint, `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33`, borrowed Runway's Storyboard-to-Film one-image-per-video pattern and routed only `Ref Image 01` into final Seedance `referenceImages[0]`; invocation `53be6385-7dfb-4f89-b0e7-c7e61e393efc` also finished `SUCCEEDED` with empty output. Raw `curl.exe` invocation of the same one-image Workflow endpoint reproduced the empty output as invocation `a6eea7bd-f8b0-4fcb-bfca-68445d3f65b6`, so this is not a Python SDK typed-field issue. Static asset diagnostic endpoint `6ce25c70-8c4e-454b-9816-3c5569aff0f3` removed the Gemini image node and routed a fixed Runway image asset into final Seedance `referenceImages[0]`; invocation `f6f358be-d4b3-44dd-a407-2fd1b06b1228` also finished `SUCCEEDED` with empty output, no failure, and no node errors. Treat Seedance `referenceImages` inside published Workflows as blocked for the hackathon path; use direct Seedance `references` or test Gen 4.5 / Veo 3.1 adapters instead.

Keep the app-facing workflow endpoint contract unchanged. The local app should still send the same 13 approved package fields. The Runway workflow should expand those fields internally:

1. Generate 9 image references from the director plan.
2. Group the images into three triptychs: `1.1-1.3`, `2.1-2.3`, and `3.1-3.3`.
3. Generate 3 short Seedance reference clips, each using one image triptych and prompt-level motion/sound direction.
4. Feed the 3 reference clips into the final Seedance hero clip if the final node exposes video-reference ports. If Workflows only exposes first/last frame ports, keep the reference clips as sidecar outputs and fold their motion beats into the final prompt.

Recommended grouping:

| Reference clip | Image references | Sound direction | Purpose | Duration |
|---|---|---|---|---|
| `Motion Ref Clip 01 - Hook Atmosphere` | `Ref Image 01-03` | Fold ambience into prompt. | Establish first-frame read, setting, and mood. | `4s` |
| `Motion Ref Clip 02 - Kinetic Build` | `Ref Image 04-06` | Fold impact/motion cues into prompt. | Establish texture, subject motion, and cause-effect action. | `4s` |
| `Motion Ref Clip 03 - Payoff Reveal` | `Ref Image 07-09` | Fold payoff accent into prompt. | Establish twist, reveal, and final thumbnail beat. | `4s` |

The three reference clips should total 12 seconds by default and never exceed 15 seconds combined.

Orderly board layout for visual inspection:

1. Keep the existing TCS Inputs, Combine chain, planner, parser, refiner, and final Seedance path in their current left-to-right order.
2. Place the nine image-reference nodes in a 3-column by 3-row board to the right of the planner/parser stage, grouped as rows: `1.1-1.3`, `2.1-2.3`, `3.1-3.3`.
3. Do not add sidecar audio nodes in the current endpoint; keep sound direction in the reference-clip prompts.
4. Place the three Seedance reference-clip nodes in a column to the right of the image board, one per row.
5. Place the final Seedance hero node furthest right and route all three reference-clip videos into its video-reference inputs when those ports are available.
6. Keep at least one node-height gap between rows and one node-width gap between columns so each stage can be inspected without overlap.

## Active Gen/Veo App Inputs

Create primitive/text input nodes for every value below. Use the exact logical names in the first column when capturing the node map.

| Logical input | Suggested Runway node name | Default test value | Expected type |
|---|---|---|---|
| `episode_id` | `TCS Input: episode_id` | `episode_001` | string |
| `audience_signal` | `TCS Input: audience_signal` | `Make the AI build a floating city powered by storms.` | string |
| `av_director_packet` | `TCS Input: av_director_packet` | JSON/text packet with audience signal, creator intent, visual anchor, motion, camera, audio, sync, and constraints. | string |
| `opening_frame_prompt` | `TCS Input: opening_frame_prompt` | `A bold 9:16 opening frame where the storm-powered floating city reads within one second.` | string |
| `motion_prompt` | `TCS Input: motion_prompt` | `Readable hook, physical storm-energy transformation, smooth reveal, clear payoff pose.` | string |
| `audio_prompt` | `TCS Input: audio_prompt` | `Native ambience, wind detail, turbine whine, transformation accent, payoff hit.` | string |
| `sync_prompt` | `TCS Input: sync_prompt` | `Lock each sound event to a visible cause and land the final hit on the payoff frame.` | string |
| `duration_seconds` | `TCS Input: duration_seconds` | `4` | string |
| `aspect_ratio` | `TCS Input: aspect_ratio` | `1080:1920` | string |
| `safety_status` | `TCS Input: safety_status` | `approved` | string |

Layout convention for the active Gen/Veo workflow graph:

- Column 1, metadata/control: `episode_id`, `duration_seconds`, `aspect_ratio`, `safety_status`.
- Column 2, audience/director packet: `audience_signal`, `av_director_packet`.
- Column 3, visual-motion cues: `opening_frame_prompt`, `motion_prompt`, optional Nano Banana/Gen-4.5 study nodes.
- Column 4, audio-sync cues: `audio_prompt`, `sync_prompt`.
- Column 5-7, prompt director: serial Combine Text chain over all 10 TCS inputs.
- Column 8, hidden director: `TCS Director: system_prompt` Text node and `TCS Director: Claude Veo prompt` node.
- Column 9, final output: Veo 3.1 final video node, with Gen-4.5 study output kept in the visual-motion lane when present.
- Keep at least one node-height gap between boxes and one node-width gap between columns. Do not stack duplicated nodes diagonally or leave newly added nodes overlapped; publish screens may visually collapse duplicated names even when the API exposes every node ID.
- Give every input node the matching default test value from the table. If every input shows the same script sample, app API submissions can still override the values, but manual Runway runs and visual inspection become misleading.
- Keep model/generation nodes to the right of input and planning stages. For checkpoints, use one functional stage per publish so endpoint behavior is easy to isolate.

Legacy Seedance workflow verifier commands below still apply when inspecting historical Seedance endpoints. They do not validate the new Gen/Veo AV packet node map yet.

Before adding the nine-image board to a legacy Seedance workflow, verify the published endpoint contract:

```powershell
uv run python scripts/verify_runway_workflow_contract.py
```

The verifier checks the local node map, published graph input nodes, serial Combine Text chain, planner/parser/refiner path, and final Seedance prompt edge. Use strict mode when you want duplicated or mismatched canvas defaults to fail the check:

```powershell
uv run python scripts/verify_runway_workflow_contract.py --strict-defaults
```

After publishing the nine-image board, verify the full image/audio/reference-clip braid:

```powershell
uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-reference-board
```

## Gen/Veo Director Node

The current Workflow checkpoint includes a text/planning node. Feed all 10 app inputs through a serial Combine Text chain, then into a Claude director node. The director returns only one compact Veo 3.1 prompt for this checkpoint; do not add parser/image-board fanout until this stage remains stable.

Use this prompt shape:

```text
You are the hidden Claude director for Top Comment Studio. The user input is one combined text block containing these 10 fields in order: episode_id, duration_seconds, aspect_ratio, safety_status, audience_signal, av_director_packet, opening_frame_prompt, motion_prompt, audio_prompt, sync_prompt. Convert them into exactly one Veo 3.1 text-to-video prompt under 950 characters. Output only the Veo prompt text, with no markdown, labels, bullets, JSON, captions, logos, watermarks, copyrighted characters, or explanatory prose. Hard priorities: native synchronized audio first, visible cause/effect action, the audience signal clearly causing the episode, safety_status honored or safely redirected, vertical 9:16, exactly 4 seconds. Use opening_frame_prompt for the first image, motion_prompt for camera/action, audio_prompt and sync_prompt for native sound timing. If fields conflict, obey: safe, 4 seconds, 9:16, native audio, no text on screen. If safety_status is rejected or needs_human_review, preserve only the safe creative spark as fictional, non-instructional, YouTube-safe imagery.
```

Graph JSON note: for Runway editor compatibility, Combine Text nodes need top-level `subTaskType: "concat"` as well as `nodeInputs.subTaskType.value: "concat"`. Without the top-level field, the internal validator may pass but the editor UI can fail to render the graph.

## Legacy Seedance Director Node

The current published canvas keeps every app input as a separate Text node, then combines those fields with a serial Combine Text chain. This is visually taller than a tree, but it keeps the API contract transparent and avoids the Workflow API scheduler issue seen with parallel Combine fan-in.

Add a Claude text/planning node. Connect the combined director brief to the text prompt and a fixed `Director System Prompt` Text node to the system prompt.

Use this prompt:

```text
You are the Runway creative director for Top Comment Studio, an audience-in-the-loop YouTube Shorts system. The creator has approved this audience signal for production. Your output is machine parsed by a JSON node. The first character of your response must be { and the last character must be }. Do not wrap the JSON in markdown. Do not use code fences. Do not write ```json. Do not add comments, prose, labels, or explanations. Return exactly one raw strict JSON object with exactly these top-level keys: seedance_prompt, image_reference_prompts, audio_reference_prompts, reference_clip_plans. Creative methodology: design one final vertical Seedance 2.0 hero clip as the product. Nano Banana Pro / Gemini 3 Pro Image references are previsual anchors, audio cues are optional texture references, and the three reference clips are motion studies that support the final hero generation. The final seedance_prompt must stand alone even if references are unavailable. Make the audience-driven mechanic visible: the top comment visibly changes the scene and the final beat invites the next safe comment. seedance_prompt must be under 950 characters and describe a safe, fictional, original, brand/logo-free 1080p 9:16 12-second Seedance clip with strong first-frame readability, clear camera motion, one coherent transformation, and an obvious payoff. image_reference_prompts must contain exactly 9 portrait 9:16 Nano Banana Pro briefs in this order: hook frame, hero subject, setting/world, palette/mood, material/texture, action pose, transition/twist, payoff/reveal, thumbnail final beat. Each image brief must be a single self-contained prompt for a still reference image with no text overlays, no logos, no copyrighted characters, and no real-person likeness. audio_reference_prompts must contain exactly 3 short sound effect briefs in this order: ambient bed, motion impact, payoff accent. reference_clip_plans must contain exactly 3 objects with keys prompt, image_indices, audio_index, duration_seconds. The three objects must group images [0,1,2], [3,4,5], [6,7,8], use audio indexes 0,1,2, and duration_seconds 4. Each reference_clip_plans prompt should describe a four-second motion study: clip 1 establishes hook and world, clip 2 shows kinetic transformation, clip 3 lands the payoff. Keep continuity across every asset: same subject, same world, same color logic, same audience-comment cause and effect. Avoid real-person impersonation, copyrighted characters, graphic harm, political persuasion, dangerous instructions, and on-screen brand marks.
```

The first validation run after adding this methodology still returned a fenced ```json block, so keep the machine-parsing sentence near the front of the prompt.

If the Workflow UI supports structured JSON output, use this shape:

```json
{
  "seedance_prompt": "",
  "image_reference_prompts": ["", "", "", "", "", "", "", "", ""],
  "audio_reference_prompts": ["", "", ""],
  "reference_clip_plans": [
    {"prompt": "", "image_indices": [0, 1, 2], "audio_index": 0, "duration_seconds": 4},
    {"prompt": "", "image_indices": [3, 4, 5], "audio_index": 1, "duration_seconds": 4},
    {"prompt": "", "image_indices": [6, 7, 8], "audio_index": 2, "duration_seconds": 4}
  ]
}
```

If structured output is awkward in the UI, create separate GPT/planner nodes for the final prompt, image prompts, audio prompts, and motion prompts. For the hackathon demo, clarity beats clever graph compression.

## Image Reference Board

Generate internal images with Nano Banana Pro / Gemini 3 Pro Image. Use high-resolution portrait output for final Seedance references, and reserve lower resolutions for quick endpoint proofs.

### JSON Example Workflow Findings

Bryan copied Runway's JSON-to-Manga example as workflow `14139cd0-d760-4ee9-9a47-90f7324f06a9` (`JSON_example`). It is useful because it shows Runway's graph-level JSON parser wiring more clearly than the UI labels.

Key graph details from version 1:

1. The JSON parser is a `workflow_text_operations` node with `subTaskType=json_parser`.
2. It defines multiple parser paths named `text[0]`, `text[1]`, etc., but the graph-level output key remains `text`.
3. Individual parsed values are selected on the edge with `from.index`, not by changing the `nodeOutput` name. For example, `from.index=1` selects `text[1]` from `nodeOutput=text`.
4. The example does not feed parser output directly into Gemini image prompts. It routes each parsed value through a `workflow_text_operations` concat node first, then sends concat `text` into Gemini `text_prompt`.
5. Gemini image reference edges use the `reference_images` input with explicit `to.index=0` for the shared style/reference image.
6. The copied example exposes the source JSON text input and the source asset image, but not the generated Gemini image outputs by default. Output exposure still needs to be checked on the publish screen and in the published endpoint graph.

Diagnostic implication for Top Comment Studio: when using one parser with multiple paths, preserve `from.index` on every outgoing edge and consider a concat node between parser output and model prompt inputs to force scalar string handoff. The earlier TCS array-to-string failures were consistent with parser output sockets/edge metadata being treated as arrays or ambiguous values. The current row-workflow approach avoids most of this by using separate scalar paths, while the next all-in-one Workflow API diagnostic should try the example pattern before assuming final Seedance is the only issue.

### Additional Example Workflow Findings

Bryan provided two more Runway workflow examples for Gemini-generated in-graph image techniques:

- `60398763-9b47-473a-8ca3-066465d39bbc` (`Storyboard to Film_example`)
- `e309a30a-364d-4bc0-ae4e-e43db1552c8a` (`JSON_StoryPanelsEX`)

Important design signals from those examples:

1. They confirm Gemini-generated images can feed downstream nodes inside Runway Workflows. Both examples chain generated Gemini images into later Gemini image nodes through `reference_images` with explicit `to.index` values.
2. Neither example uses Seedance. The Storyboard-to-Film example sends generated Gemini images into `workflow_kling_3_0_standard` video nodes, not into Seedance.
3. The Storyboard-to-Film video pattern is one generated image per video node. Each Kling node receives one `referenceImages[0]` edge plus a per-shot motion prompt from a Gemini text node, with 5-second duration and `1280x720` resolution.
4. The StoryPanels example is an image-panel graph only. It uses static asset input images plus Gemini Pro image nodes at varied aspect ratios (`16:9`, `3:4`, `9:16`, `21:9`) and does not expose generated outputs by default.
5. Output exposure is not a reliable clue in copied examples: both inspected example graphs had `exposed=0`, so TCS must continue checking the publish screen and published endpoint graph for every intended output.

TCS implication: borrow the examples' one-reference-image-per-video-shot structure for future sidecar reference clips, but do not assume the same handoff works with Seedance. Endpoint `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33` tested the nearest Seedance equivalent, a single generated Gemini image into one Seedance `referenceImages[0]`, and still returned empty output. The next Workflow API diagnostic should use a static uploaded asset or direct image URL as the Seedance reference input; if that also returns empty, keep Seedance references in the direct API lane and use Workflows for prompt-only hero clips and exposed image boards.

API-safe contract notes from the Runway docs:

- Nano Banana Pro / Gemini 3 Pro Image's API model slug is `gemini_image3_pro`.
- Nano Banana / Gemini 2.5 Flash's fast fallback API model slug is `gemini_2.5_flash`.
- The text/image-to-image endpoint uses `model`, `promptText`, `ratio`, and optional `referenceImages`.
- Useful direct Nano Banana Pro portrait ratios include `768:1344`, `1536:2752`, and `3072:5504`. Use `1536:2752` for direct Seedance first-frame handoffs, `3072:5504` for max-quality previsuals that will be resized or compressed before direct handoff, and `768:1344` only for quick proofs. Keep `1080:1920` as the app's logical Shorts aspect and Seedance workflow input, not as the direct Gemini image ratio.
- Nano Banana Pro supports up to 14 reference images and 1K, 2K, or 4K output.
- If a published workflow graph shows a GPT image node with `appNodeType: gpt-tidepool-alpha`, do not expose or route that node into Seedance for endpoint tests. Manual node runs in the Runway canvas can still succeed, but published workflow API invocations can fail with `No model variant mapping for app node type: gpt-tidepool-alpha`.

Preferred image nodes:

1. `Ref Image 01 - Hook Frame`
2. `Ref Image 02 - Hero Subject`
3. `Ref Image 03 - Setting World`
4. `Ref Image 04 - Palette Mood`
5. `Ref Image 05 - Material Texture`
6. `Ref Image 06 - Action Pose`
7. `Ref Image 07 - Transition Twist`
8. `Ref Image 08 - Payoff Reveal`
9. `Ref Image 09 - Thumbnail Beat`

The earlier published v1 used three GPT image nodes, but those resolved to the unsupported `gpt-tidepool-alpha` app node type in workflow API runs. A fresh explicit `GPT Image 2 Text/Image to Image` node can generate manually in the Runway canvas, but the first V1.1 endpoint still published and failed under `appNodeType: gpt-tidepool-alpha`. The combined serial prompt test endpoint `ec5e1e70-0406-41e2-9195-08ef5e32f7c4` failed the same way, so the hackathon image lane should use Nano Banana Pro / Gemini 3 Pro Image through `gemini_image3_pro` before expanding to nine image nodes in three visual groups:

1. Hook atmosphere: `Ref Image 01 - Hook Frame`, `Ref Image 02 - Hero Subject`, `Ref Image 03 - Setting World`.
2. Kinetic build: `Ref Image 04 - Palette Mood`, `Ref Image 05 - Material Texture`, `Ref Image 06 - Action Pose`.
3. Payoff reveal: `Ref Image 07 - Transition Twist`, `Ref Image 08 - Payoff Reveal`, `Ref Image 09 - Thumbnail Beat`.

## Sidecar Audio Status

Sidecar audio is disabled in the current known-good text-only endpoint.

Removed sidecar nodes:

1. `Audio Cue 01 - Ambient Bed`, 4-5 seconds.
2. `Audio Cue 02 - Motion Impact`, 2-4 seconds.
3. `Audio Cue 03 - Payoff Accent`, 2-3 seconds.

The live Seedance 2.0 Workflows node exposes `generateAudio` but not a direct audio-reference input port. Current endpoint `e4a221ab-743d-45ac-bc47-633d66227614` uses the historically successful text-only graph, leaves Seedance's built-in Generate Audio setting enabled, and keeps sound-design direction in the final prompt. Reintroduce SFX nodes only if a future Seedance node exposes audio-reference ports or the edit package needs separate audio assets.

## Incremental Checkpoints

The active rebuild is intentionally staged from the smallest proven Workflow API endpoint upward:

1. `5d1d6d5f-c194-4aaf-841a-bf68fa618425`: true two-node Seedance proof, `script -> Seedance`, returned one MP4.
2. `82d1f2da-0ed8-4bdc-8888-9c804852c2c1`: restored all 13 app inputs around the same Seedance path, returned one MP4.
3. `eee1e1d2-71e8-4cc5-a516-416ee71e1f89`: polished non-overlapping 13-input layout, returned one MP4.
4. `07eab094-6c6a-46a4-9dfb-963d97a293f5`: added hidden system prompt Text, Claude JSON planner, and Parse JSON `seedance_prompt` stage before Seedance. This planner/parser checkpoint completed through the Workflow API with one Seedance MP4 output.
5. `ff2496e8-f10b-4b2a-a98a-fa474bc0b599`: added a wide parallel Combine Text fan-in and a second Claude refiner, but returned `SUCCEEDED` with empty output and Combine node errors saying `Node is already running in this execution`.
6. `e4a221ab-743d-45ac-bc47-633d66227614`: rewired the Combine Text layer as a single serial chain through all 13 app inputs, kept the second Claude refiner after Parse JSON, and completed through the Workflow API with one Seedance MP4 output. Keep image and reference clips deferred until a separate tiny image/reference endpoint proves API-safe execution.
7. `b9beb013-0fe5-4f20-b244-a39b788ae95d`: added one 5-second Seedance 2.0 sidecar node, `TCS Motion Ref Clip 01: Seedance proof`, fed by the existing Claude refiner `text`. This endpoint completed through the Workflow API with two Seedance MP4 outputs: one final hero clip and one sidecar proof clip.
8. `ec5e1e70-0406-41e2-9195-08ef5e32f7c4`: wired one GPT Image 2 node serially into final Seedance `firstFrame` and wired the proven sidecar Seedance clip into final Seedance `referenceVideos`. Invocation `23af7906-76c5-448f-8884-a6357025d924` reported `No model variant mapping for app node type: gpt-tidepool-alpha`, confirming GPT Image 2 remains blocked in published Workflow API execution.
9. Direct Nano Banana Pro API proof: `POST /v1/text_to_image` with `model=gemini_image3_pro` and portrait `ratio=768:1344` returned task `8f46769b-92d3-4412-8c96-89d5d4445f25`, which completed `SUCCEEDED` with one image output. The same prompt with `1080:1920` returned a validation error, so keep `1080:1920` for the app/Seedance logical aspect and use Gemini's own accepted ratios for direct image tasks. A `3072:5504` proof, task `07d79876-b8df-4d9b-b0e9-07f63f19c357`, also completed, but direct Seedance `promptImage` rejected the raw PNG as larger than 16 MB; use `1536:2752` for direct handoff unless the image is resized/compressed first.
10. Direct Seedance first-frame handoff checkpoint: `POST /v1/text_to_image` at `1536:2752` produced Nano Banana task `6abcc1e7-81ec-42fc-90e5-b0277e134d3f`, then `POST /v1/image_to_video` with `model=seedance2`, `promptImage=[{"uri": nano_banana_output_url, "position": "first"}]`, vertical `ratio=720:1280`, and a 5-second duration produced Seedance task `83e7205d-7e4f-4f8c-81ad-50b963fc0f66`, which completed `SUCCEEDED` with one video output. This proves one high-resolution Nano Banana image can become a Seedance first frame before rebuilding a full workflow image board.
11. Corrected input-default publish: endpoint `691b3f2b-720c-4b45-ade1-3190a45b11d5` republishes the safe sidecar Seedance workflow with distinct TCS Input defaults. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults` passes against this endpoint, so it is the clean baseline before adding the nine-image board.
12. Nine-image board publish: endpoint `d5e3926d-2ddd-40b0-894b-726780fcefdd` adds nine `gemini-image-3-pro` image-reference nodes, three `eleven-text-to-sfx` audio cues, and three four-second Seedance reference clips arranged as three visual rows. This checkpoint proved the parser-to-image and parser-to-audio prompt handoffs, but was superseded because the three final `referenceVideos` edges were missing explicit indexes.
13. Indexed reference-video board publish: endpoint `bfb8bc80-47c6-45bd-829d-b817414d10b9` keeps the same orderly nine-image/audio/reference-clip board and adds explicit `referenceVideos` indexes `0`, `1`, and `2` on the final Seedance node. Runway's internal validator returned `valid: true`, but live invocation `e7c9478a-a6c3-4065-83c5-d14da1ab32e7` failed because JSON parser outputs named `text[0]` arrived as arrays at image and SFX prompt inputs.
14. Scalar JSON-key publish: endpoint `104f35ec-11b9-4e33-b9e1-ff7a6507e190` changed planner output to top-level string keys, but parser output name `text[0]` still produced array-shaped handoffs. Live invocation `5c782174-ca40-4387-96e1-94d9ffc604bf` failed with the same array-to-string prompt errors.
15. Parser-output-name publish: endpoint `cfe53adb-2804-485d-adda-ae073626b0d0` changed JSON parser path output names to `text`. Live invocation `974f5e16-aa0f-478b-ac82-56666d268b62` was still `RUNNING` at last check with 3 outputs, 0 node errors, and no failure.
16. Sidecar-free board publish: endpoint `1827e99b-ea37-44f2-8525-45c5e299369d` removes the three audio parser nodes and three `eleven-text-to-sfx` nodes, keeps final Seedance `generateAudio` enabled, and routes all three reference clips into final Seedance `referenceVideos`. It passed graph verification, but live invocation `bfad2308-18e1-44d9-910e-f5ebafa8a39e` stalled at 87.5% with no outputs or failure after the three plain text-to-video reference clips likely completed.
17. Sidecar-only reference-clip publish: endpoint `afd546a3-dbdb-4372-8aff-3a9c0e5282e8` keeps the nine Nano Banana image refs and three Seedance reference clips, exposes the reference clips as sidecar outputs, disables final Seedance `referenceVideos`, and keeps final Seedance `generateAudio` enabled. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-reference-board` passes, but live invocation `97703298-5d9b-4048-9ef4-b47050fed0a5` stalled at 72.5%. Since the graph has 40 runnable nodes, 72.5% maps to 29/40 and likely sits inside the nine-image Nano Banana board before sidecar or final Seedance outputs complete.
18. Keyframe-only fast-path publish: endpoint `8923373c-fee1-4506-94b5-b9b8bd13370a` removes sidecar clips and seven of nine image refs. It keeps the serial Combine/Claude planner/refiner path, generates only `Ref Image 01` and `Ref Image 09`, feeds them into final Seedance `firstFrame`/`lastFrame`, disables final `referenceImages` and `referenceVideos`, and keeps final Seedance `generateAudio` enabled. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-keyframe-only` passes. Live invocation `f2071527-86b9-4471-81e3-ee769f20f051` crossed the 72.5% wall and reached 80%, then finished `SUCCEEDED` with no exposed outputs.
19. Text-only fallback publish: endpoint `9c0f1f38-e664-4b9e-9402-f2dae15b692b` removes image refs, sidecar clips, sidecar audio, final `referenceImages`, and final `referenceVideos`. It matches the previously proven serial Combine/Claude/refiner/final Seedance shape: final Seedance receives only the refined prompt as `textPrompt`, exposes `video`, and keeps `generateAudio` enabled. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults` passes, but live invocation `4732c4b5-f714-48bf-8b8c-a5d0ac5f96d9` finished `SUCCEEDED` with no exposed outputs.
20. Known-good endpoint restore: endpoint `e4a221ab-743d-45ac-bc47-633d66227614` is the current local `.env` checkpoint because historical app invocation `de9c70e6-972a-44ca-ae16-119d3d1ab762` and fresh app invocation `414d3a5a-8554-4b8b-ae31-2b2853c6f920` both returned one final Seedance MP4. It has duplicated canvas defaults, so use it through the local app route where all 13 inputs are overridden, not manual Runway default runs.
21. Image-board row-1 publish: endpoint `f4ed6cf3-69b0-436b-a37c-82e1a7eeeb46` starts the separate image-board workflow lane. It keeps the same 13 app input/serial Combine/Claude planner contract, parses `image_reference_prompts[0..2]`, generates only `Ref Image 01-03`, exposes all three `image` outputs, and removes final Seedance plus sidecar reference clips. Direct invocation `d99becc7-1da3-489a-a94e-c1bd4c693621` completed `SUCCEEDED` with three image outputs.
22. Image-board row-2 publish: endpoint `06a818f1-6dec-4cae-878d-ceeb6fbd5c2d` keeps the same board-only graph shape, parses `image_reference_prompts[3..5]`, generates `Ref Image 04-06`, and exposes all three `image` outputs. Direct invocation `f7360924-0e1f-479d-a223-0d53ff901813` completed `SUCCEEDED` with three image outputs.
23. Image-board row-3 publish: endpoint `fd051825-a295-4406-a80b-1fbfd8f8b7da` keeps the same board-only graph shape, parses `image_reference_prompts[6..8]`, generates `Ref Image 07-09`, and exposes all three `image` outputs. Direct invocation `dcfe5d44-e8f7-4bbf-9fdc-0da897b5f0ae` completed `SUCCEEDED` with three image outputs.
24. Nine-image final reference checkpoint: endpoint `8ab20d96-444e-4751-aa91-9c0b44c5036c` was published from editor version 267. It keeps the 13 input/serial Combine/Claude planner/refiner path and nine Nano Banana image nodes, removes sidecar audio and motion reference clips, removes final `firstFrame`, `lastFrame`, and `referenceVideos` edges, and routes all nine image outputs into final Seedance `referenceImages` with indexes `0..8`. Final Seedance video and all nine image outputs are exposed in the graph. Live invocation `f030c851-4eea-41ce-b3a3-7a5b3f86658d` crossed the earlier 72.5% and 87.5% stall bands, then finished `SUCCEEDED` with empty output, no failure, and no node-error metadata. Direct API task `5bf9b443-cdf0-443c-b752-9e292592e69b` remains the proven MP4 proof using the same nine existing image URLs through `POST /v1/text_to_video` `references`; it completed `SUCCEEDED` with one MP4 output.
25. Parser-normalized no-audio checkpoint: endpoint `2866261a-9e0c-434e-8e32-b41da06ef9d4` was published from editor version 270 after comparing against Runway's `JSON_example` workflow. It inserts nine `workflow_text_operations` concat nodes between the image JSON parsers and Gemini image prompts, sets every image parser outgoing edge to `from.index=0`, keeps final `referenceImages` indexes `0..8`, and disables final Seedance `generateAudio`. Published graph version 272 retained 9 normalizers, 9 parser edges with `from.index`, final `generateAudio=false`, and final `video` exposed. Live invocation `a2c33089-e7f0-48c5-bfaa-e531dff83833` still finished `SUCCEEDED` with empty output and no failure, so the all-in-one issue is not fixed by parser normalization or disabling generated audio.
26. One-image Gemini-to-Seedance reference diagnostic: endpoint `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33` was published from editor version 273 after inspecting Runway's `Storyboard to Film_example` and `JSON_StoryPanelsEX` examples. It removes 8 of 9 image nodes, exposes `TCS Ref Image 01`, routes that one generated Gemini image into final Seedance `referenceImages[0]`, disables final `generateAudio`, sets final duration to 5 seconds, and exposes final `video`. Live invocation `53be6385-7dfb-4f89-b0e7-c7e61e393efc` completed `SUCCEEDED` with empty output and no failure metadata. This narrows the Workflow API issue to generated-Gemini-image-to-Seedance-reference handoff, not just nine-reference overload, parser normalization, or generated audio.
27. Curl SDK-bypass diagnostic: Runway's Seedance guide notes that SDK types may lag Seedance-specific fields and recommends curl for current tests. Script `scripts/run_seedance_curl_diagnostic.ps1` now submits/polls Seedance direct tasks and Workflow invocations with raw `curl.exe` while printing only sanitized status metadata. Direct curl `POST /v1/text_to_video` with one image reference completed as task `b988c359-4afe-4609-875c-e484b410e57d`, `SUCCEEDED` with one output. Raw curl `POST /v1/workflows/7ab7c6c7-6f54-4d40-a838-63fa72b1fe33` created invocation `a6eea7bd-f8b0-4fcb-bfca-68445d3f65b6`, which completed `SUCCEEDED` with empty output. Therefore curl confirms the direct Seedance image-reference route while reproducing the one-image Workflow failure without the Python SDK or the local `httpx` wrapper.
28. Static asset Seedance reference diagnostic: endpoint `6ce25c70-8c4e-454b-9816-3c5569aff0f3` was published from editor version 275. It keeps the 13-input serial Combine/planner/refiner path, removes the Gemini image node/parser/normalizer, adds a fixed Runway `asset-node` image, routes that asset into final Seedance `referenceImages[0]`, disables final `generateAudio`, sets final duration to 5 seconds, and exposes final `video`. Raw curl invocation `f6f358be-d4b3-44dd-a407-2fd1b06b1228` reached 75% and completed `SUCCEEDED` with empty output, no failure, and no node-error metadata. This means the Workflow issue is broader than generated Gemini image handoff: Seedance `referenceImages` inside published Workflows should be treated as unreliable until Runway fixes or documents the path.

## Image Board Lane

Keep the image board separate from the hero MP4 workflow. The stable app endpoint should stay on `e4a221ab-743d-45ac-bc47-633d66227614` until a richer hero workflow is proven independently.

The package page now has a dedicated "Nine-image reference board" lane. It submits the three row workflows, refreshes their statuses, displays the nine returned image thumbnails, and can submit a board-referenced Seedance MP4 task once all nine images are available and creator approval is checked.

Current board proof:

```text
RUNWAY_IMAGE_BOARD_WORKFLOW_ID=f4ed6cf3-69b0-436b-a37c-82e1a7eeeb46
```

Current board row endpoints:

```text
RUNWAY_IMAGE_BOARD_ROW_1_WORKFLOW_ID=f4ed6cf3-69b0-436b-a37c-82e1a7eeeb46
RUNWAY_IMAGE_BOARD_ROW_2_WORKFLOW_ID=06a818f1-6dec-4cae-878d-ceeb6fbd5c2d
RUNWAY_IMAGE_BOARD_ROW_3_WORKFLOW_ID=fd051825-a295-4406-a80b-1fbfd8f8b7da
```

This endpoint should return three exposed image outputs for the first visual row:

1. `TCS Ref Image 01 (1.1) - Hook Frame`
2. `TCS Ref Image 02 (1.2) - Hero Subject`
3. `TCS Ref Image 03 (1.3) - Setting World`

All three row endpoints have succeeded once, producing nine total images across three invocations. The app orchestrates them as a nine-image board package, then uses the direct Seedance text-to-video image-reference route for the final MP4 attempt. Keep the published all-in-one workflow endpoint `8ab20d96-444e-4751-aa91-9c0b44c5036c` as a diagnostic checkpoint, because its first live invocation completed with empty output even though the direct `references` task returned the MP4.

Seedance image-reference MP4 proof in progress:

```text
TASK_ID=5bf9b443-cdf0-443c-b752-9e292592e69b
API=POST /v1/text_to_video
PAYLOAD_SHAPE={"model":"seedance2","ratio":"720:1280","duration":10,"references":[{"uri":"..."}]}
RESULT=SUCCEEDED with 1 MP4 output
WORKFLOW_ENDPOINT_DIAGNOSTIC=8ab20d96-444e-4751-aa91-9c0b44c5036c
WORKFLOW_INVOCATION=f030c851-4eea-41ce-b3a3-7a5b3f86658d SUCCEEDED with empty output
NORMALIZED_WORKFLOW_ENDPOINT=2866261a-9e0c-434e-8e32-b41da06ef9d4
NORMALIZED_WORKFLOW_INVOCATION=a2c33089-e7f0-48c5-bfaa-e531dff83833 SUCCEEDED with empty output
ONE_IMAGE_WORKFLOW_ENDPOINT=7ab7c6c7-6f54-4d40-a838-63fa72b1fe33
ONE_IMAGE_WORKFLOW_INVOCATION=53be6385-7dfb-4f89-b0e7-c7e61e393efc SUCCEEDED with empty output
CURL_DIRECT_TASK=b988c359-4afe-4609-875c-e484b410e57d SUCCEEDED with 1 MP4 output
CURL_WORKFLOW_INVOCATION=a6eea7bd-f8b0-4fcb-bfca-68445d3f65b6 SUCCEEDED with empty output
STATIC_ASSET_WORKFLOW_ENDPOINT=6ce25c70-8c4e-454b-9816-3c5569aff0f3
STATIC_ASSET_WORKFLOW_INVOCATION=f6f358be-d4b3-44dd-a407-2fd1b06b1228 SUCCEEDED with empty output
```

Status check command:

```bash
uv run python scripts/run_runway_image_board_rows.py --status row1=d99becc7-1da3-489a-a94e-c1bd4c693621 row2=f7360924-0e1f-479d-a223-0d53ff901813 row3=dcfe5d44-e8f7-4bbf-9fdc-0da897b5f0ae
```

Curl diagnostic commands:

```powershell
./scripts/run_seedance_curl_diagnostic.ps1 -Mode direct -ReferenceCount 1 -Duration 5
./scripts/run_seedance_curl_diagnostic.ps1 -Mode task-status -Id <task_id>
./scripts/run_seedance_curl_diagnostic.ps1 -Mode workflow -WorkflowId 7ab7c6c7-6f54-4d40-a838-63fa72b1fe33
./scripts/run_seedance_curl_diagnostic.ps1 -Mode workflow-status -Id <workflow_invocation_id>
```

## Reference Clip Nodes

Add three short Seedance 2.0 reference-clip nodes before the final hero clip. Keep combined duration at or below 15 seconds.

Preferred reference clip nodes:

1. `Motion Ref Clip 01 - Hook Atmosphere`, 4 seconds.
2. `Motion Ref Clip 02 - Kinetic Build`, 4 seconds.
3. `Motion Ref Clip 03 - Payoff Reveal`, 4 seconds.

Each reference clip should receive the corresponding `reference_clip_plans.*.prompt` from Parse JSON. If the node exposes more than first/last image ports, connect all three images in the group. If it exposes only first/last image ports, connect the first and third image and describe the middle image in the clip prompt. While sidecar audio is disabled, keep sound direction as text inside the reference-clip prompt.

The previous audio cues used `audio_reference_prompts[*]` and Runway's text-to-sound contract: `POST /v1/sound_effect` with `model=eleven_text_to_sound_v2`, `promptText`, optional `duration`, and optional `loop`. Those nodes are removed from the current endpoint to reduce output complexity while Seedance generated audio is evaluated.

Keep the three reference clips exposed as sidecar outputs in the larger board unless a new published endpoint proves `referenceVideos` works without stalling. For demo reliability, current endpoint `e4a221ab-743d-45ac-bc47-633d66227614` removes sidecar clips and image refs entirely, returning to the historically successful final prompt-only route. Build image-board workflows as separate lanes so board failures never block the hero MP4. The Seedance docs describe video references for text-to-video, while our final workflow node also uses first/last image keyframes; endpoint `1827e99b-ea37-44f2-8525-45c5e299369d` stalled when those modes were mixed.

## Final Seedance Node

Add a final Seedance 2.0 text-to-video node.

Settings:

- Model: `seedance2` / Seedance 2.0.
- Prompt: director `seedance_prompt` from Parse JSON output 1.
- Duration: set to `12s`.
- Aspect ratio: set to `9:16`.
- Resolution: set to `1080p`.
- First frame: connect `Ref Image 01` or the first frame of `Motion Ref Clip 01`.
- Last frame: connect `Ref Image 09` or the final frame of `Motion Ref Clip 03`.
- Audio: keep Generate Audio enabled unless the node exposes reliable audio-reference ports.
- Video references: keep final `referenceVideos` disabled until a smaller proof shows they work without stalling. The current text-only endpoint also disables image refs and sidecar clips so the final hero clip is not blocked by extra reference-generation branches.

Final prompt fallback if structured output is not available:

```text
Create a vertical cinematic Seedance 2.0 hero clip for Top Comment Studio. The audience selected: {{selected_comment}}. Safe creative interpretation: {{safe_interpretation}}. Tone: {{target_tone}}. Style: {{visual_style}}. Use a fast first-frame hook, clear silhouettes, storm-powered motion, a smooth camera reveal, readable cause-and-effect, and a satisfying final payoff. Keep all content fictional, original, safe, logo-free, and suitable for a general YouTube Shorts audience. End with a visual that invites: {{next_cta}}
```

## Publish Checklist

1. Create the workflow in the Runway Workflows page.
2. Name it `TCS Seedance Director v1`.
3. Add all app input nodes listed in this guide.
4. Add the director node and reference-generation nodes.
5. Add the final Seedance 2.0 node.
6. Run the workflow once with the default floating-city values.
7. Confirm the output is a vertical 10-15 second hero clip.
8. Publish the workflow.
9. Open the Developer Portal workflow registry.
10. Copy the published workflow UUID.
11. Retrieve or inspect the graph schema and capture input node IDs.
12. Add `RUNWAY_WORKFLOW_ID` and `RUNWAY_WORKFLOW_NODE_MAP_JSON` to local `.env`.
13. Restart the local FastAPI app so settings reload.
14. Generate or open a package, confirm the Runway handoff panel has no configuration blockers, check creator approval, and submit.

## Published V1 Endpoint

Published endpoint UUID:

```text
961b51c3-6d75-408f-b98c-464728c829b4
```

Current known-good text-only checkpoint for local `.env`:

```text
RUNWAY_WORKFLOW_ID=e4a221ab-743d-45ac-bc47-633d66227614
```

Newly published text-only fallback checkpoint, now superseded because it returned no exposed output:

```text
RUNWAY_WORKFLOW_ID=9c0f1f38-e664-4b9e-9402-f2dae15b692b
```

Previous keyframe-only fast-path checkpoint, now superseded by the text-only endpoint:

```text
RUNWAY_WORKFLOW_ID=8923373c-fee1-4506-94b5-b9b8bd13370a
```

Previous sidecar-only nine-image/reference-clip checkpoint, now superseded by the keyframe-only endpoint:

```text
RUNWAY_WORKFLOW_ID=afd546a3-dbdb-4372-8aff-3a9c0e5282e8
```

Previous final-reference-video checkpoint, now superseded by the sidecar-only endpoint:

```text
RUNWAY_WORKFLOW_ID=1827e99b-ea37-44f2-8525-45c5e299369d
```

Corrected input-default sidecar proof checkpoint:

```text
RUNWAY_WORKFLOW_ID=691b3f2b-720c-4b45-ade1-3190a45b11d5
```

Original sidecar reference-clip proof checkpoint:

```text
RUNWAY_WORKFLOW_ID=b9beb013-0fe5-4f20-b244-a39b788ae95d
```

Text-only rich checkpoint:

```text
RUNWAY_WORKFLOW_ID=e4a221ab-743d-45ac-bc47-633d66227614
```

Original output-fixed v1 endpoint:

```text
RUNWAY_WORKFLOW_ID=961b51c3-6d75-408f-b98c-464728c829b4
```

## Node Map Template

The app expects `RUNWAY_WORKFLOW_NODE_MAP_JSON` to be one JSON object. Published Runway Text input nodes use `prompt` as their output key.

```json
{
  "episode_id": {"node_id": "52b5f5ee-2ceb-49d3-ba2f-b32a6ac9c70b", "output_key": "prompt"},
  "selected_comment": {"node_id": "75a34fca-37b5-4373-aa08-48ae1bd1980e", "output_key": "prompt"},
  "safe_interpretation": {"node_id": "b7cdc4c4-cb08-4eee-abf9-5f43fdefe910", "output_key": "prompt"},
  "previous_video_summary": {"node_id": "54919bd1-5146-4aa9-b6e8-9dd0164a3d33", "output_key": "prompt"},
  "previous_video_cta": {"node_id": "30b7f5b1-61cb-4745-a15b-f9aa9af5c5aa", "output_key": "prompt"},
  "target_tone": {"node_id": "78db2704-d753-4757-9387-e825ce9d8683", "output_key": "prompt"},
  "visual_style": {"node_id": "66af515a-2aab-4a07-938c-608a80606351", "output_key": "prompt"},
  "creative_notes": {"node_id": "dae7a62d-c61c-470d-a2b6-4f8a74794731", "output_key": "prompt"},
  "script": {"node_id": "0fb93ec3-f453-47bd-8e92-d1d4a6e6e815", "output_key": "prompt"},
  "next_cta": {"node_id": "d0a89e18-ab40-4b82-9b13-aabc97f34c60", "output_key": "prompt"},
  "duration_seconds": {"node_id": "227dedd0-834d-4dd7-ae74-d69d96ce8146", "output_key": "prompt"},
  "aspect_ratio": {"node_id": "b60ca32f-00a1-475f-ab4f-7914bd33cabf", "output_key": "prompt"},
  "safety_status": {"node_id": "bd6043cd-f900-42ef-b062-5abd99729134", "output_key": "prompt"}
}
```

For local `.env`, keep it on one line:

```text
RUNWAY_WORKFLOW_NODE_MAP_JSON={"episode_id":{"node_id":"52b5f5ee-2ceb-49d3-ba2f-b32a6ac9c70b","output_key":"prompt"},"selected_comment":{"node_id":"75a34fca-37b5-4373-aa08-48ae1bd1980e","output_key":"prompt"},"safe_interpretation":{"node_id":"b7cdc4c4-cb08-4eee-abf9-5f43fdefe910","output_key":"prompt"},"previous_video_summary":{"node_id":"54919bd1-5146-4aa9-b6e8-9dd0164a3d33","output_key":"prompt"},"previous_video_cta":{"node_id":"30b7f5b1-61cb-4745-a15b-f9aa9af5c5aa","output_key":"prompt"},"target_tone":{"node_id":"78db2704-d753-4757-9387-e825ce9d8683","output_key":"prompt"},"visual_style":{"node_id":"66af515a-2aab-4a07-938c-608a80606351","output_key":"prompt"},"creative_notes":{"node_id":"dae7a62d-c61c-470d-a2b6-4f8a74794731","output_key":"prompt"},"script":{"node_id":"0fb93ec3-f453-47bd-8e92-d1d4a6e6e815","output_key":"prompt"},"next_cta":{"node_id":"d0a89e18-ab40-4b82-9b13-aabc97f34c60","output_key":"prompt"},"duration_seconds":{"node_id":"227dedd0-834d-4dd7-ae74-d69d96ce8146","output_key":"prompt"},"aspect_ratio":{"node_id":"b60ca32f-00a1-475f-ab4f-7914bd33cabf","output_key":"prompt"},"safety_status":{"node_id":"bd6043cd-f900-42ef-b062-5abd99729134","output_key":"prompt"}}
```

## Schema Fetch Helper

After publishing, this PowerShell command can retrieve the workflow graph for node ID capture. It assumes `.env` values are loaded into the shell environment.

```powershell
$headers = @{
    Authorization = "Bearer $env:RUNWAYML_HACKATHON_API_SECRET"
    "X-Runway-Version" = "2024-11-06"
}
Invoke-RestMethod "https://api.dev.runwayml.com/v1/workflows/$env:RUNWAY_WORKFLOW_ID" -Headers $headers |
    ConvertTo-Json -Depth 40
```

Do not paste real API secrets into docs or commits.
