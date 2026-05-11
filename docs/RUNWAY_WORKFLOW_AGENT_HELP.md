# Runway Workflow Agent Help

This is the short recovery note for future agents when conversation context is compacted or lost. Read this before changing Runway workflow code, building a new Runway graph, or debugging a published workflow endpoint.

## First Principles

Top Comment Studio is a Python/FastAPI hackathon app using `uv`. Keep the app runnable, keep Bryan in the creator-approval loop, and preserve the Audience-in-the-Loop short-form MVP direction.

Runway has two different workflow surfaces that are easy to confuse:

1. Runway app workflow canvas: `https://app.runwayml.com/.../ai-tools/workflows/{canvas_workflow_id}/edit`. This is where graphs are visually edited, validated, run, and published. The browser app talks to internal `https://api.runwayml.com/v1/dynamic_workflows/...` endpoints. Treat those as an authenticated editor surface, not the stable app integration API. Do not commit cookies, session exports, or browser storage.
2. Runway Developer API: `https://api.dev.runwayml.com`. This is what app code should call with `Authorization: Bearer <RUNWAYML_HACKATHON_API_SECRET>` and `X-Runway-Version: 2024-11-06`. Published workflow endpoints are invoked through this surface.

Canvas workflow IDs and published endpoint IDs are different. A 404 from `/v1/workflows/{id}` often means the canvas ID was used where the published endpoint UUID was needed.

## Current App Contract

The current app-side Runway workflow contract lives in `src/top_comment_studio/runway/workflows.py`.

Required logical inputs:

```text
episode_id
audience_signal
av_director_packet
opening_frame_prompt
motion_prompt
audio_prompt
sync_prompt
duration_seconds
aspect_ratio
safety_status
```

Every published workflow intended for the app should expose one primitive Text input node per logical input. Name the node and exposed output label exactly like this:

```text
TCS Input: episode_id
TCS Input: audience_signal
...
```

The live Text input output key is normally `prompt`. Configure local `.env` with the published endpoint ID and a node map:

```json
{
  "episode_id": {"node_id": "published-graph-node-uuid", "output_key": "prompt"},
  "audience_signal": {"node_id": "published-graph-node-uuid", "output_key": "prompt"}
}
```

The app builds `nodeOutputs` for `POST /v1/workflows/{workflow_id}`:

```json
{
  "nodeOutputs": {
    "published-graph-node-uuid": {
      "prompt": {
        "type": "primitive",
        "value": "episode_001"
      }
    }
  }
}
```

After submission, poll `GET /v1/workflow_invocations/{invocation_id}`. Direct model tasks use `GET /v1/tasks/{task_id}` instead.

## Programmatic Build Pattern

Use this sequence when creating or rebuilding Runway workflows:

1. Start from a tiny proven graph. A two-node text input to video node is better than a full board on the first publish.
2. Delete disconnected or abandoned nodes before publishing. Disconnected nodes can still schedule and fail in published workflow runs.
3. Add externally controlled values as distinct Text inputs with unique defaults and exposed `prompt` outputs.
4. Publish, retrieve the published graph, capture the published node IDs, and update `RUNWAY_WORKFLOW_NODE_MAP_JSON`.
5. Run the verifier before spending more generation credits.
6. Add one functional stage per checkpoint: serial Combine chain, planner, parser, image board, sidecar clips, final video. Publish and run each checkpoint before expanding again.

The useful mental model is: build visually in the Runway canvas, publish to create a Developer API endpoint, then interact programmatically through `nodeOutputs` and polling. Use internal dynamic workflow requests only for authenticated canvas inspection or automation experiments, and document any such experiment before relying on it.

Keep the canvas readable as you build. Arrange nodes left to right by domain: controls/metadata, audience and AV packet, visual-motion cues, audio-sync cues, then final Gen/Veo output. Move each newly created node into its lane before renaming or filling it; overlapped Runway nodes can steal focus and cause edits to land on the wrong node.

## Programmatic Workflow Engineering Notes

When automating Runway workflow builds, treat the graph as data with a visual editor attached. The internal canvas API can validate, save, and publish a graph, but the Developer API endpoint that the app calls is the only integration contract that matters after publishing.

Observed internal canvas calls:

```text
GET  https://api.runwayml.com/v1/dynamic_workflows/{canvas_workflow_id}/versions/latest
POST https://api.runwayml.com/v1/dynamic_workflows/validate
POST https://api.runwayml.com/v1/dynamic_workflows/{canvas_workflow_id}/versions
POST https://api.runwayml.com/v1/dynamic_workflows_devportal_published
GET  https://api.runwayml.com/v1/dynamic_workflows_featured/{featured_workflow_id}
```

Use browser-captured auth only for the current local editing session. Never paste bearer tokens, cookies, workspace headers, or signed asset URLs into docs, commits, memory, or chat summaries. It is fine to record canvas IDs, published endpoint IDs, invocation IDs, featured workflow IDs, node names, and local artifact paths.

Safe save/publish sequence:

1. Fetch the latest canvas version and work from that graph.
2. Apply a narrow graph mutation: add a stage, correct node inputs, adjust layout, or expose outputs.
3. Run internal `/dynamic_workflows/validate` on the full graph.
4. Save a new canvas version with the latest server version number.
5. Publish that saved version to the Developer Portal.
6. Retrieve `GET /v1/workflows/{published_endpoint_id}` from `api.dev.runwayml.com`.
7. Verify the published graph, not just the saved canvas graph.
8. Run one paid smoke only after static checks pass.

The version 65 checkpoint proved why step 6 matters: the saved canvas had the correct 1080p graph, but the published endpoint dropped TCS input labels and the exposed final output. Version 66 fixed those publish fields and became the usable checkpoint.

Graph mutation rules that have held up:

- Preserve stable node names. Use `TCS Input: ...`, `TCS Storyboard ...`, `TCS Photo Enhance ...`, and `TCS Continuity Core ...` names as anchors for scripts and verifiers.
- Preserve node IDs unless a node must be replaced. App node maps and verifier expectations are easier to maintain when existing input nodes remain stable.
- Keep every externally supplied value as a primitive Text node output named `prompt`.
- For Text/Combine nodes, include both top-level `subTaskType: "concat"` and `nodeInputs.subTaskType.value = "concat"` when writing graph JSON.
- For JSON parser fanout, route parser output key `text` with edge `from.index`; do not invent output keys like `text[0]` for downstream prompt fields.
- Normalize parser fanout through a concat/text node before model prompt inputs when the receiving node expects a scalar string.
- Use scalar Veo frame inputs: generated image output -> `startFrame`; adjacent transition target image -> `endFrame`. Do not use indexed `promptImage[0]` inside Workflow Veo nodes.
- Expose exactly the outputs the app or demo needs. Terminal generated nodes may appear in the publish UI by default, while connected nodes may disappear from output selection.
- Delete disconnected model nodes before publishing. Published invocations can still schedule disconnected generation branches.

Known Workflow app node type values:

| Purpose | Task type | Runtime-safe `appNodeType` | Notes |
|---|---|---|---|
| Gemini Image Pro / Nano Banana Pro | `workflow_gemini_image` | `gemini-image-3-pro` | Use model value `gemini-3-pro-image-preview` in Workflow nodes. |
| Gemini API text/vision analysis | `workflow_gemini_api` | `gemini` | `gemini-api` can validate and publish but failed paid runtime. |
| Gen-4.5 image-to-video | `workflow_gen4_5` | `gen4_5-image-to-video` | Use for silent cinematic studies, not final native-audio output. |
| Veo 3.1 standard video | `workflow_veo3_1` | `veo-3.1` | Proven with `seconds=4`, `aspectRatio=9:16`, `noAudio=false`. |
| Veo 3.1 keyframes | `workflow_veo3_1` | `veo-3.1-keyframes` | Proven for segments with scalar `startFrame` and `endFrame`. |
| Stitch Videos | `workflow_media_processing_v2` | `stitch-video` | Input key `input`, output key `video`. |

Resolution lessons:

- `resolution=720p` produced 720x1280 MP4s for 9:16 Veo Workflow segments.
- `resolution=1080p` validated and paid-smoked successfully in version 66, producing true 1080x1920 H.264 + AAC output.
- Keep the logical app aspect as `1080:1920`, but Workflow Veo aspect remains `9:16`.

Featured workflow harvesting is useful, but copy patterns rather than blindly copying whole graphs:

- `661` Storyboard to Film supplied the continuity-spine idea: one storyboard JSON, identity/world anchor, sequential frames, video shots, final assembly.
- `596` Photo Enhancer supplied the two-pass Gemini analysis + image enhancement chain between storyboard frames and video references.
- `529` Story Panels supplied continuity language for panels that should read as one evolving scene.
- `364` Seamless Transitions supplied the adjacent-keyframe idea: each video starts on one frame and lands on the next.

When adapting a featured workflow, inspect node names, task types, `appNodeType`, `nodeInputs`, output exposure, and edge indexes. Rebuild the smallest TCS-shaped version first, then publish and smoke it before copying more structure.

Current Gen/Veo Continuity Core checkpoint:

- Canvas workflow: `ba325b07-a845-4fe6-901e-9242666ef8c7` (`TCS Gen/Veo Storyboard-to-Short v1`).
- 1080p seamless-keyframe paid-proven endpoint: `c1b49d17-c80f-4705-b0e6-86c89a070464`, published workflow version 66.
- 1080p seamless-keyframe graph shape: 68 nodes, 131 edges, 10 exposed TCS inputs, same version 63 seamless keyframe routing, plus a cleaner left-to-right layout for generated frames, Photo Enhancer passes, Veo segments, and stitches. Each beat still routes `TCS Storyboard Frame 0N` -> `TCS Photo Enhance 0N: final enhanced frame` -> matching Veo 3.1 segment scalar `startFrame`; additionally enhanced frame 02 feeds segment 01 `endFrame`, enhanced frame 03 feeds segment 02 `endFrame`, and enhanced frame 04 feeds segment 03 `endFrame`. The first three Veo nodes use `appNodeType: veo-3.1-keyframes`, `workflow-veo3-1-keyframes-task`, and `resolution=1080p`; the final payoff segment uses `appNodeType: veo-3.1`, `workflow-veo3-1-task`, and `resolution=1080p`.
- 1080p seamless-keyframe static verification: internal Runway `/v1/dynamic_workflows/validate` passed; Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains --require-seamless-transition-keyframes --require-1080p-video`.
- 1080p seamless-keyframe paid live test: version 66 paid invocation `f805c55d-4ed3-461a-ac82-1153c828904b` completed `SUCCEEDED`, returned one MP4, and reported empty node errors. `ffprobe` found H.264 video at 1080x1920 for about 16.042 seconds plus AAC audio for about 16.085 seconds. Downloaded artifact: `data/local/runway_outputs/f805c55d-4ed3-461a-ac82-1153c828904b_6e092b87-1cef-4b69-8a78-3a62fb08869f_item_1.mp4`; contact sheet: `data/local/runway_outputs/f805c55d-4ed3-461a-ac82-1153c828904b_contact_sheet.jpg`; safe result note: `data/local/runway_outputs/f805c55d-4ed3-461a-ac82-1153c828904b_result.json`.
- Do not use intermediate endpoint `c5882933-e837-432d-b59e-d255be020d29` from version 65. It saved the 1080p/layout graph, but the published Developer API endpoint dropped input labels and the exposed final output; version 66 fixed those publish fields.
- Previous 720p seamless-keyframe fallback endpoint: `65e09485-4169-41d9-9282-85b52148949f`, published workflow version 63.
- Previous photo-enhanced fallback endpoint: `277aecec-43a4-4042-844e-e9e3d41db8d3`, published workflow version 62.
- Previous photo-enhanced graph shape: 68 nodes, 128 edges, 10 exposed TCS inputs, same version 59 Continuity Core spine, plus the Runway featured workflow `596` Photo Enhancer method after each Gemini storyboard frame. Each beat routes `TCS Storyboard Frame 0N` -> `TCS Photo Enhance 0N: analysis pass 1` -> `prompt pass 1` -> `first pass image` -> `analysis pass 2` -> `prompt pass 2` -> `final enhanced frame` -> Veo 3.1 segment scalar `startFrame`.
- Previous photo-enhanced static verification: internal Runway `/v1/dynamic_workflows/validate` passed; Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains`.
- Previous photo-enhanced paid live test: version 62 paid invocation `cc30e6ea-f938-45b7-8d56-8ac62c314c67` completed `SUCCEEDED`, returned one MP4, and reported no node errors. `ffprobe` found H.264 video at 720x1280 for about 16.042 seconds plus AAC audio for about 16.085 seconds. Downloaded artifact: `data/local/runway_outputs/cc30e6ea-f938-45b7-8d56-8ac62c314c67_6e092b87-1cef-4b69-8a78-3a62fb08869f_item_1.mp4`; contact sheet: `data/local/runway_outputs/cc30e6ea-f938-45b7-8d56-8ac62c314c67_contact_sheet.jpg`; safe result note: `data/local/runway_outputs/cc30e6ea-f938-45b7-8d56-8ac62c314c67_result.json`.
- Runtime lesson: version 61 endpoint `6e9bac23-016f-4f40-857e-d846132623ac` paid invocation `147f5d4f-bd19-454b-a223-2a1ba3d1f2e3` finished without MP4 output because the Gemini API nodes used `appNodeType: gemini-api`; version 62 uses `appNodeType: gemini`.
- Previous paid-proven baseline endpoint: `31f64606-73bf-4b43-ba53-596e92fc26bd`, published workflow version 59.
- Previous paid-proven baseline graph shape: 41 nodes, 72 edges, 10 exposed TCS inputs, serial Combine chain, outer `TCS Director: system_prompt` + `TCS Director: Claude Veo prompt`, outer `TCS Asset Planner: system_prompt` + `TCS Asset Planner: board/sidecar/segments JSON` + `TCS Asset Parser: boards sidecars segments`, `TCS Asset Planner: parsed creative map`, `TCS Continuity Core: enriched creative brief`, then the paid-proven storyboard director/parser/anchor/four frames/four Veo 3.1 `startFrame` segments/stitches/final output spine.
- Exposed output: `final_storyboard_short_16s` from `TCS Storyboard Final: stitched 16s short`.
- Paid-proven static verification: internal Runway `/v1/dynamic_workflows/validate` passed before save/publish; Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core`.
- Paid live test: version 59 paid invocation `cc086bdd-3a14-4290-a6e8-bbb7c7f10788` completed `SUCCEEDED`, returned one MP4, and reported no node errors. `ffprobe` found H.264 video at 720x1280 for about 16.042 seconds plus AAC audio for about 16.085 seconds. Downloaded artifact: `data/local/runway_outputs/cc086bdd-3a14-4290-a6e8-bbb7c7f10788_6e092b87-1cef-4b69-8a78-3a62fb08869f_item_1.mp4`; contact sheet: `data/local/runway_outputs/cc086bdd-3a14-4290-a6e8-bbb7c7f10788_contact_sheet.jpg`; safe result note: `data/local/runway_outputs/cc086bdd-3a14-4290-a6e8-bbb7c7f10788_result.json`.
- Creative read: version 66 is the strongest continuity checkpoint so far. The storm-powered floating structure remains centered and recognizable across the contact sheet, the keyframe landings reduce the sense of four unrelated clips, and the sequence moves from charged storm blues into a warm golden payoff at 1080x1920. Version 63 remains the paid-proven 720p fallback if 1080p cost or latency becomes a rehearsal issue.
- Design note: the outer director and asset planner now improve the continuity core through text planning before image/video generation. Do not reconnect the old independent director-preview/asset-media branch to the final output unless Bryan explicitly approves the larger credit spend and the continuity risk.
- Visual layout note: canvas version 58 is a layout-only save after the version 57 paid smoke. It moves all 40 nodes into clean left-to-right lanes and does not change the published endpoint. Key lanes: inputs -> Combine chain -> outer Director/Asset Planner -> `TCS Continuity Core: enriched creative brief` -> storyboard director/parser/anchor -> four frames -> four Veo `startFrame` segments -> stitches -> final output.
- Parser wiring note: canvas/published version 59 adds `TCS Asset Planner: parsed creative map`. All 17 parser outputs (`board_prompts.0-8`, `sidecar_prompts.0-2`, `segment_prompts.0-3`, `continuity_notes`) feed this map node, and the map feeds the Continuity Core as input index 2. This makes the Asset Planner structurally part of the final creative prompt path.

Previous Gen/Veo Storyboard-to-Short checkpoint:

- Canvas workflow: `ba325b07-a845-4fe6-901e-9242666ef8c7` (`TCS Gen/Veo Storyboard-to-Short v1`).
- Published endpoint: `4af4b372-b117-49bd-9a7e-4812430f76eb`, published workflow version 56.
- Graph shape: 34 nodes, 47 edges, 10 exposed TCS inputs, serial Combine chain, one hidden Storyboard Director system prompt, one Claude storyboard JSON node, one JSON parser, one hidden identity/world anchor image, four sequential storyboard frames, four Veo 3.1 image-to-video segment nodes, two intermediate Stitch Videos nodes, and one final Stitch Videos node.
- Exposed output: `final_storyboard_short_16s` from `TCS Storyboard Final: stitched 16s short`.
- Static verification: `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-storyboard-to-short` passed against the published graph.
- Paid live test: invocation `4b700e61-d835-433b-b330-5f58f2cefa8f` completed `SUCCEEDED`, returned one MP4, no node errors. `ffprobe` found about 16 seconds of H.264 video plus AAC audio. Downloaded artifact: `data/local/runway_outputs/4b700e61-d835-433b-b330-5f58f2cefa8f_final_storyboard_short_16s.mp4`; contact sheet: `data/local/runway_outputs/4b700e61-d835-433b-b330-5f58f2cefa8f_contact_sheet.jpg`.
- Runtime lesson: Workflow Veo 3.1 I2V expects the generated frame on scalar `startFrame`. Version 55 endpoint `1766f759-d1ec-4cce-9a82-7386e8a72983` used indexed `promptImage[0]`; paid invocation `b994efd0-6c3a-427d-a539-7ffe87c384d3` reported `Invalid task options: startFrame: Invalid input: expected object, received undefined` while still showing `RUNNING`.
- Creative read: continuity is much better than the prior branch-stitch design. The contact sheet keeps a consistent illustrated storm world and floating-city payoff, though the first beat introduces a small robot guide before the city becomes the main subject.

Previous Gen/Veo final-master checkpoint:

- Canvas workflow: `ba325b07-a845-4fe6-901e-9242666ef8c7` (`TCS Gen/Veo AV Director v1`).
- Published endpoint: `26bf091b-6f75-49c4-bd74-4de137eef9ce`, published workflow version 54.
- Graph shape: 48 nodes, 54 edges, 10 exposed TCS inputs, preserved serial Combine + Claude director + Veo 3.1 preview lane, hidden asset-planner Claude node, JSON parser with 16 outputs, 9 hidden/terminal Nano Banana Pro board panels, 3 hidden sidecar-start image references, 3 hidden Gen-4.5 sidecar videos, 4 Veo 3.1 native-audio segment videos, and 4 Stitch Videos nodes.
- Exposed output: `final_final_video_20s` from `TCS Final Final: director + asset master`.
- Static verification: Developer API retrieval confirmed 48 nodes, 54 edges, 10 exposed inputs, 1 exposed generated output, and no workflow nodes missing `appNodeType`.
- Paid live test: invocation `ce9d109c-8a3b-4fcf-9ae3-0ad1ecf6d16d` completed `SUCCEEDED`, returned one MP4, no node errors. `ffprobe` found about 20 seconds of H.264 video plus AAC audio. Contact-sheet review showed weak creative continuity because the final stitch combined the 4-second director-preview branch with the independently planned 16-second asset branch.
- Superseded by the version 56 Storyboard-to-Short endpoint above. Keep this endpoint only as a regression/debug checkpoint for the earlier branch-stitch architecture.

Previous exposed-assets Gen/Veo checkpoint:

- Canvas workflow: `ba325b07-a845-4fe6-901e-9242666ef8c7` (`TCS Gen/Veo AV Director v1`).
- Published endpoint: `c38549da-a2b8-4541-96a0-db14af640184`, published workflow version 52.
- Graph shape: 47 nodes, 52 edges, 10 exposed TCS inputs, preserved serial Combine + Claude director + Veo 3.1 preview lane, hidden asset-planner Claude node, JSON parser with 16 outputs, 9 terminal Nano Banana Pro board panels, 3 hidden sidecar-start image references, 3 Gen-4.5 sidecar videos, 4 Veo 3.1 native-audio segment videos, and 3 Stitch Videos nodes.
- Exposed outputs: `final_video_4s_preview`, `board_panel_01` through `board_panel_09`, `sidecar_shot_01` through `sidecar_shot_03`, and `long_final_video_16s`.
- Static verification: Developer API retrieval confirmed 47 nodes, 52 edges, 10 exposed inputs, 14 exposed outputs, and no workflow nodes missing `appNodeType`.
- Paid live test: not run yet. A full invocation currently schedules 13 image generations, 7 video generations, and stitch operations.

Previous Gen/Veo director-stage checkpoint:

- Canvas workflow: `ba325b07-a845-4fe6-901e-9242666ef8c7` (`TCS Gen/Veo AV Director v1`).
- Published endpoint: `9ed1d223-c002-4f4d-b750-c43f0f3de8d8`, published workflow version 41.
- Graph shape: 22 nodes, 21 edges, 10 exposed TCS inputs, 9 serial Combine Text nodes, one hidden `TCS Director: system_prompt` Text node, one Claude director node, and one Veo 3.1 final node.
- Final output: `final_video` from the Veo node.
- Proven settings: `seconds=4`, `aspectRatio=9:16`, `resolution=720p`, `noAudio=false`.
- Successful invocation: `201a6753-3100-4b01-92fb-14698be41309`, returned one MP4, no node errors; `ffprobe` found H.264 video and AAC audio.

## Graph Lessons Already Paid For

Keep these lessons. They cost time and credits.

- Prefer a serial Combine Text chain over a wide parallel fan-in. Endpoint `ff2496e8-f10b-4b2a-a98a-fa474bc0b599` returned Combine errors like `Node is already running in this execution`.
- If writing Runway graph JSON directly, native Combine Text nodes need both `nodeInputs.subTaskType.value = "concat"` and top-level `subTaskType = "concat"`. The Developer API validator accepted nodes without the top-level field, but the Runway editor UI could not render them.
- Keep planner prompts strict when a JSON parser follows them. Put the instruction near the front: first character must be `{`, last character must be `}`, no Markdown fences, no prose.
- For JSON parser fanout, Runway's example pattern uses parser output key `text` plus edge `from.index` to select `text[0]`, `text[1]`, etc. Do not rely on output names like `text[0]` as model prompt inputs. If a downstream model expects a scalar string, route parser output through a concat/text-normalizer first.
- Expose intended outputs on the publish screen. Runway examples often have generated outputs unexposed by default, and `SUCCEEDED` with empty output can be an exposure problem or a model handoff problem.
- Give every TCS input a distinct canvas default. API submissions override defaults, but duplicate defaults make manual runs and graph inspection misleading.
- Keep at least one full node-height gap between rows and one node-width gap between functional columns. Do not leave newly added nodes stacked on the canvas origin; inspect positions before saving or publishing.
- The Runway Workflow canvas Veo 3.1 node rejected `seconds=10` with `Invalid task options: seconds: Invalid input` on endpoint `fb490b2c-aa0e-4e31-95eb-12b88c7bc6fc`. Use `seconds=4` for the current Workflow checkpoint unless the canvas UI proves another value.
- Inspect the published graph, not just the editor canvas. The public graph is what the app runs.
- Avoid published GPT Image workflow nodes that resolve to `appNodeType: gpt-tidepool-alpha`. They produced `No model variant mapping for app node type: gpt-tidepool-alpha` even when wired serially.
- Gemini/Nano Banana Pro Workflow image nodes must publish with `appNodeType: "gemini-image-3-pro"`; copied JSON-example image nodes can render in the editor without it but fail Developer Portal publishing with `Version has nodes without app node types`.
- The publish UI auto-lists generated outputs from nodes without outgoing connectors. If a board image feeds a sidecar start frame, it may disappear from the output list; keep the visible board nodes terminal and use hidden duplicate start-frame image nodes for sidecars when all 9 board panels must be exposed.
- Ephemeral uploads are a Developer API asset-staging feature, not a graph merge operation. Use them when local/downloaded files need `runway://` URIs for a second-stage API call; inside one Workflow, combine generated videos with graph wiring such as Stitch Videos and expose only the final node.
- Keep Workflow image generation and final image-referenced video as separate lanes unless a new proof says otherwise.

## Current Reliable Lanes

The current hackathon direction is Gen/Veo first:

- Image generation: Nano Banana Pro / Gemini 3 Pro Image, API model `gemini_image3_pro`.
- Fast image fallback: Nano Banana / Gemini 2.5 Flash, API model `gemini_2.5_flash`.
- Silent cinematic shot studies: Gen-4.5, API model `gen4.5`.
- Final native-sound video: Veo 3.1, API model `veo3.1`.

Useful public API calls are implemented in `src/top_comment_studio/runway/client.py`:

```text
POST /v1/text_to_image
POST /v1/image_to_video
POST /v1/text_to_video
POST /v1/workflows/{workflow_id}
GET  /v1/workflow_invocations/{invocation_id}
GET  /v1/tasks/{task_id}
```

Use these ratios and limits unless current Runway docs say otherwise:

- Gemini image direct portrait quick proof: `768:1344`.
- Gemini image direct handoff: `1536:2752`.
- Gemini max previsual: `3072:5504`, but resize/compress before video handoff because raw PNGs can exceed a 16 MB asset limit.
- App logical Shorts aspect: `1080:1920`.
- Public vertical video ratio for Gen-4.5/Veo: `720:1280`.
- Public Gen-4.5/Veo duration: 2-10 seconds.

Historical Seedance facts are still useful for debugging older endpoints, but do not build new demo paths around Seedance unless Bryan asks. Direct Seedance image-reference tasks worked, but Seedance `referenceImages` inside published Workflows repeatedly finished `SUCCEEDED` with empty outputs.

## Proven And Diagnostic IDs

Keep these IDs as breadcrumbs, not as secrets:

- Known-good legacy prompt-only Seedance Workflow endpoint: `e4a221ab-743d-45ac-bc47-633d66227614`.
- Current Gen/Veo director-stage endpoint: `9ed1d223-c002-4f4d-b750-c43f0f3de8d8`.
- Previous grouped Gen/Veo one-edge checkpoint: `35a20104-42a9-4339-90b3-0b1e65259667`.
- Legacy sidecar proof endpoint: `b9beb013-0fe5-4f20-b244-a39b788ae95d`.
- Corrected legacy input-default checkpoint: `691b3f2b-720c-4b45-ade1-3190a45b11d5`.
- Proven image-board row workflows: row 1 `f4ed6cf3-69b0-436b-a37c-82e1a7eeeb46`, row 2 `06a818f1-6dec-4cae-878d-ceeb6fbd5c2d`, row 3 `fd051825-a295-4406-a80b-1fbfd8f8b7da`.
- Direct Seedance nine-reference task proof: `5bf9b443-cdf0-443c-b752-9e292592e69b`.
- Raw curl direct Seedance one-reference proof: `b988c359-4afe-4609-875c-e484b410e57d`.
- Workflow Seedance reference failures: `8ab20d96-444e-4751-aa91-9c0b44c5036c`, `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33`, `6ce25c70-8c4e-454b-9816-3c5569aff0f3`.

Detailed history lives in `docs/RUNWAY_RESOURCES.md`, `docs/RUNWAY_WORKFLOW_BUILD_GUIDE.md`, and repo memory under `/memories/repo/runway_workflow_checkpoints.md`.

## Validation Commands

Run the light repo audit after meaningful setup/doc changes:

```powershell
uv run python scripts/agent_repo_audit.py
```

Run tests when app code or Runway payload code changes:

```powershell
uv run pytest
```

Verify a published workflow contract after setting `RUNWAYML_HACKATHON_API_SECRET`, `RUNWAY_WORKFLOW_ID`, and `RUNWAY_WORKFLOW_NODE_MAP_JSON`:

```powershell
uv run python scripts/verify_runway_workflow_contract.py --strict-defaults
```

For the current Gen/Veo final-master endpoint:

```powershell
uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-final-master
```

For the next Storyboard-to-Short checkpoint:

```powershell
uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-storyboard-to-short
```

For the Continuity Core checkpoint:

```powershell
uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core
```

For the older board-row workflow lane:

```powershell
uv run python scripts/run_runway_image_board_rows.py --submit --chain main --episode episode_003
uv run python scripts/run_runway_image_board_rows.py --status row1=<invocation_id> row2=<invocation_id> row3=<invocation_id>
```

For Seedance direct-vs-workflow diagnostics with curl:

```powershell
.\scripts\run_seedance_curl_diagnostic.ps1 -Mode direct -Episode episode_003 -ReferenceCount 1 -Duration 5
.\scripts\run_seedance_curl_diagnostic.ps1 -Mode workflow -WorkflowId <workflow_id> -Episode episode_003
.\scripts\run_seedance_curl_diagnostic.ps1 -Mode task-status -Id <task_id>
.\scripts\run_seedance_curl_diagnostic.ps1 -Mode workflow-status -Id <workflow_invocation_id>
```

## Debugging Checklist

When a workflow breaks:

1. Confirm the ID is the published Developer API endpoint ID, not the app canvas ID.
2. Confirm the API secret and `X-Runway-Version` header.
3. Retrieve the published graph and compare input node IDs to `RUNWAY_WORKFLOW_NODE_MAP_JSON`.
4. Check that every intended output is exposed in the published endpoint.
5. Inspect `failure`, `failureCode`, `progress`, `output`, and node-error metadata on the invocation.
6. If Workflow invocation returns `SUCCEEDED` with empty output, reproduce with raw curl before blaming Python SDK types.
7. If parser output reaches image, SFX, or video prompt fields, normalize to scalar text before the model node.
8. If a model node fails only when published, inspect `appNodeType` in the published graph and compare it with documented public API model slugs.

Do not spend generation credits on large all-in-one graphs until the smaller checkpoint proves the same handoff.
