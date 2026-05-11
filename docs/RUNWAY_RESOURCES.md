# Runway Resources Inventory

This document keeps the Runway API and GitHub resources close at hand for Top Comment Studio. Do not store secrets here. The local hackathon Runway key belongs in `.env` as `RUNWAYML_HACKATHON_API_SECRET`.

## Hackathon

- API Hackathon: https://runwayml.com/api-hackathon
- Terms: https://runwayml.com/api-hackathon-terms
- Submission deadline from the hackathon page: Monday, May 11, 2026 at 9am ET.
- Submission expects a short project description and demo video.
- Judging criteria: creativity, technical depth, impact, polish.

## API Basics

- Developer docs: https://docs.dev.runwayml.com/
- Developer portal: https://dev.runwayml.com/
- API reference: https://docs.dev.runwayml.com/api
- Base URL: `https://api.dev.runwayml.com`
- Auth header: `Authorization: Bearer <RUNWAYML_HACKATHON_API_SECRET>`
- Version header: `X-Runway-Version: 2024-11-06`

## Runway Account Surfaces

The project has access to two signed-in Runway surfaces during local development:

- Runway app workflows: https://app.runwayml.com/video-tools/teams/techmandesign/ai-tools/workflows
- Runway Developer Portal: https://dev.runwayml.com/
- Custom workflow API endpoints: https://dev.runwayml.com/organization/8f8366b8-b7b6-4f9c-baae-f72c16c9f79f/workflows

Do not commit browser cookies, storage state, login exports, or session files. Local cookie/session exports are intentionally ignored by `.gitignore`.

## Developer Portal Model Catalog

The Developer Portal currently exposes these model/feature shortcuts for Top Comment Studio planning:

- `runway/gwm-avatars` - real-time interactive avatars powered by GWM-1.
- `runway/Gen-4.5` - text-to-video and image-to-video.
- `runway/Gen-4 Turbo` - fast image-to-video.
- `runway/Gen-4 Aleph` - video-to-video editing, transformation, and generation.
- `runway/Gen-4 Image` - text/image-to-image generation.
- `runway/Gen-4 Image Turbo` - faster, more cost-efficient text/image-to-image generation.
- `runway/Gen-3 Turbo` - legacy image-to-video.
- `runway/Act Two` - motion capture, image/video-to-video.
- `google/Gemini 3 Pro` / Nano Banana Pro - image generation with 4K support; API model slug `gemini_image3_pro`.
- `google/Gemini 2.5 Flash` / Nano Banana - faster image generation and editing fallback; API model slug `gemini_2.5_flash`.
- `openai/GPT Image 2` - image generation up to 4K; API model slug `gpt_image_2`, but avoid current Workflow image nodes that publish as `appNodeType: gpt-tidepool-alpha`.
- `google/Veo 3` and `google/Veo 3.1` - text/image-to-video with sound.
- `elevenlabs/Text to Speech` - speech generation.
- `elevenlabs/Voice Isolation` - background noise removal.
- `elevenlabs/Sound Effect` - text-to-audio effects.
- `elevenlabs/Voice Dubbing` - audio translation/dubbing.
- `elevenlabs/Speech to Speech` - voice conversion while preserving tone.

## Runway App Workflows

The Runway app has a node-based Workflows area for chaining models and intermediate steps. Useful featured templates to inspect or clone for the Top Comment Studio pipeline include:

- Story Panels
- B Roll Generator
- Seamless Transitions
- New Angles
- Storyboard to Film
- Video to Video - Scene Edit
- Video to Video - Style Transfer
- Fabric, Color, Texture Swap

Initial workflow direction: create a custom workflow that takes a reviewed top-comment creative seed, generates storyboard panels or reference images, produces a vertical video draft, and optionally adds voiceover/sound effects after creator approval.

Detailed build/publish guide for the first workflow:

- [RUNWAY_WORKFLOW_BUILD_GUIDE.md](RUNWAY_WORKFLOW_BUILD_GUIDE.md)

Preferred hackathon model stack:

- LLM text generation: GPT 5.5
- Image generation: Nano Banana Pro / Gemini 3 Pro Image (`gemini_image3_pro` in the API)
- Fast image fallback: Nano Banana / Gemini 2.5 Flash (`gemini_2.5_flash` in the API)
- Silent cinematic shot studies: Runway Gen-4.5 (`gen4.5`) through image-to-video
- Final sound-enabled video: Google Veo 3.1 (`veo3.1`) through image-to-video or text-to-video

Current hackathon adapter rule: do not build new demo paths around Seedance. Use Nano Banana Pro for the nine-image board, optionally upscale those images only after a documented Precision v2/upscaler endpoint is confirmed, use Gen-4.5 for silent movie-shot studies, and use Veo 3.1 for the final video because the demo output needs sound.

### First Published Workflow Contract

Working name: `TCS Gen/Veo Director v2`.

Goal: turn one approved Top Comment Studio package into one polished vertical final video with sound. The app now builds a unified Gen/Veo audio-video director packet instead of preserving the Seedance-shaped 13-input method. The packet keeps the audience signal and creator approval loop, then combines visual anchor, subject continuity, scene world, motion, camera language, audio design, audio-video sync, and negative constraints into one shared scene contract. As of the current docs, Gen-4.5 and Veo 3.1 image-to-video accept one prompt image, so the app passes the board's first hero image as `promptImage` and compresses the remaining board plus AV packet into the prompt.

App-provided logical inputs that need published workflow node mappings:

- `episode_id`
- `audience_signal`
- `av_director_packet`
- `opening_frame_prompt`
- `motion_prompt`
- `audio_prompt`
- `sync_prompt`
- `duration_seconds`
- `aspect_ratio`
- `safety_status`

Local app configuration after publishing:

```text
RUNWAY_WORKFLOW_ID=published_workflow_uuid
RUNWAY_WORKFLOW_NAME="TCS Gen/Veo Director v2"
RUNWAY_WORKFLOW_NODE_MAP_JSON={"episode_id":{"node_id":"node-uuid","output_key":"prompt"}}
```

`RUNWAY_WORKFLOW_NODE_MAP_JSON` must include every logical input above. Each entry maps the app field name to a published workflow input node ID and output key. The live Runway Text input nodes use `prompt` as their output key. The local app builds `nodeOutputs` for `POST /v1/workflows/{id}` and then polls `GET /v1/workflow_invocations/{id}` on demand.

Current diagnostic endpoint UUID:

```text
e4a221ab-743d-45ac-bc47-633d66227614
```

This endpoint is retained as a historical fallback/diagnostic only. It is not the current hackathon final-video path.

Diagnostic history:

- `8ae9c852-4319-417c-9d08-f389570b5db1`: V1.1 graph with GPT Image 2 branch; Workflow API invocation failed the image node as `gpt-tidepool-alpha` and returned empty output.
- `4cec124c-3217-4435-844c-0b794dc2cdcc`: GPT Image isolated and hidden; parsed Claude JSON fed Seedance directly, but Workflow API still returned `SUCCEEDED` with empty output.
- `34abb3cb-1f88-4a2a-b5d4-3fc0888e9c36`: Direct Seedance diagnostic where `TCS Input: script` feeds Seedance `textPrompt`, but disconnected nodes remained and could still schedule.
- `45745fae-baed-498c-b84e-84c9ff5549bb`: One-edge endpoint with disconnected nodes still present; invocation `4290417d-7633-457f-8651-6de272fc3a69` showed disconnected Claude still executed and failed with undefined prompt.
- `5d1d6d5f-c194-4aaf-841a-bf68fa618425`: True two-node Seedance endpoint with only `TCS Input: script -> Seedance 2.0`; minimal Workflow API path succeeded. Invocation `ba15f8c4-8363-4a6d-b16f-a117daf3b605` returned one Seedance MP4 URL with zero node errors.
- `82d1f2da-0ed8-4bdc-8888-9c804852c2c1`: 13-input checkpoint rebuilt upward from the successful two-node base. Published graph has 14 nodes, 1 edge, 13 exposed text prompts, and only original `script` connected to Seedance. App invocation `86d47202-4abe-4a40-8833-fd96947349c9` completed `SUCCEEDED` with one Seedance MP4 output and zero node errors.
- `eee1e1d2-71e8-4cc5-a516-416ee71e1f89`: Polished 13-input layout checkpoint. Published graph has 14 nodes, 1 edge, 13 uniquely named exposed text prompts arranged into non-overlapping input groups, and only `script` connected to Seedance. App invocation `54d26e50-af62-4f2e-b936-a37a08a8a15c` completed `SUCCEEDED` with one Seedance MP4 output and zero node errors.
- `07eab094-6c6a-46a4-9dfb-963d97a293f5`: Planner/parser checkpoint. Published graph has 17 nodes and 4 edges: hidden system prompt Text -> Claude `system_prompt`, `script` -> Claude `prompt`, Claude `text` -> Parse JSON `text`, and Parse JSON `text[0]` -> Seedance `textPrompt`. The 13 app text inputs remain exposed with stable node IDs, internal planner/parser nodes are hidden, and Seedance `video` is exposed. App invocation `e1888b11-d1d5-4078-af20-c583746bad48` completed `SUCCEEDED` with one Seedance MP4 output.
- `ff2496e8-f10b-4b2a-a98a-fa474bc0b599`: Wide parallel Combine Text + Claude refiner checkpoint. Published graph had 31 nodes and 30 edges, but invocation `1eb5bf3b-ef8d-4c21-9968-9dd77eecb545` returned `SUCCEEDED` with empty output and Combine node errors: `Node is already running in this execution`.
- `e4a221ab-743d-45ac-bc47-633d66227614`: Current known-good serial Combine Text + Claude refiner checkpoint. Published graph has 31 nodes and 30 edges: 12 serial `text-concat` nodes combine all 13 app inputs, hidden planner system Text -> planner Claude JSON, Parse JSON `seedance_prompt`, hidden refinement system Text -> refiner Claude, and refiner Claude `text` -> final Seedance `textPrompt`. The 13 app text inputs remain exposed with stable node IDs, internal system prompts are hidden, and Seedance `video` is exposed. App invocation `de9c70e6-972a-44ca-ae16-119d3d1ab762` completed `SUCCEEDED` with one Seedance MP4 output and zero node errors. Fresh app invocation `414d3a5a-8554-4b8b-ae31-2b2853c6f920` also completed `SUCCEEDED` with one video output. Canvas defaults are duplicated, but app submissions override every input.
- `b9beb013-0fe5-4f20-b244-a39b788ae95d`: Sidecar Seedance reference-clip proof. Published graph has 32 nodes and 31 edges: the serial Combine/Claude/refiner/final Seedance path remains intact, plus one 5-second `TCS Motion Ref Clip 01: Seedance proof` node fed by the refiner Claude `text`. The 13 app text inputs remain exposed with stable node IDs, final Seedance `video` is exposed, and the sidecar proof `video` is exposed. App invocation `06ee71a5-3e6e-4b36-ade3-7d199bada83a` completed `SUCCEEDED` with two Seedance MP4 outputs and zero node errors.
- `691b3f2b-720c-4b45-ade1-3190a45b11d5`: Corrected input-default publish of the sidecar Seedance reference-clip proof. The node IDs and serial Combine-to-planner wiring remain stable, and `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults` passes with all 13 TCS Input defaults distinct.
- `d5e3926d-2ddd-40b0-894b-726780fcefdd`: Initial nine-image board checkpoint. Published graph adds nine Nano Banana Pro / Gemini Image 3 Pro nodes (`gemini-image-3-pro`), three Text to SFX nodes (`eleven-text-to-sfx`), and three four-second Seedance reference clips in orderly rows. Superseded by `bfb8bc80-47c6-45bd-829d-b817414d10b9` because the final `referenceVideos` edges needed explicit indexes.
- `bfb8bc80-47c6-45bd-829d-b817414d10b9`: Indexed nine-image/audio/reference-clip board checkpoint. Same 61-node, 74-edge board, with final Seedance `referenceVideos` edges indexed `0`, `1`, and `2`. Runway internal validation returned `valid: true`, and the verifier passed, but live invocation `e7c9478a-a6c3-4065-83c5-d14da1ab32e7` failed because JSON parser outputs named `text[0]` arrived as arrays at image and SFX prompt inputs.
- `104f35ec-11b9-4e33-b9e1-ff7a6507e190`: Scalar JSON-key checkpoint. The planner emitted top-level string keys instead of arrays, but parser outputs still used the `text[0]` output name. Live invocation `5c782174-ca40-4387-96e1-94d9ffc604bf` failed with the same array-to-string prompt errors.
- `cfe53adb-2804-485d-adda-ae073626b0d0`: Parser-output-name checkpoint. JSON parser path entries use output name `text` instead of `text[0]`, which removes the array-shaped prompt handoff. Live invocation `974f5e16-aa0f-478b-ac82-56666d268b62` was still `RUNNING` at last check with 3 outputs, 0 node errors, and no failure.
- `1827e99b-ea37-44f2-8525-45c5e299369d`: Sidecar-free nine-image/reference-clip checkpoint. The graph removes the three audio parser nodes and three `eleven-text-to-sfx` sidecar nodes, keeps the nine Nano Banana Pro image refs and three Seedance reference clips, routes those clips into final Seedance `referenceVideos`, and keeps final Seedance `generateAudio` enabled. Live invocation `bfad2308-18e1-44d9-910e-f5ebafa8a39e` stalled at 87.5% with no outputs/failure, likely at the final mixed keyframe + reference-video Seedance node.
- `afd546a3-dbdb-4372-8aff-3a9c0e5282e8`: Sidecar-only reference-clip checkpoint. The graph keeps the nine Nano Banana image refs and three Seedance reference clips, exposes reference clips as sidecar outputs, disables final Seedance `referenceVideos`, and keeps final Seedance `generateAudio` enabled. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-reference-board` passes, but live invocation `97703298-5d9b-4048-9ef4-b47050fed0a5` stalled at 72.5%. The graph has 40 runnable nodes, so 72.5% maps to 29/40 and likely sits inside the nine-image Nano Banana board before sidecar or final Seedance outputs complete.
- `8923373c-fee1-4506-94b5-b9b8bd13370a`: Keyframe-only fast-path checkpoint. The graph removes sidecar audio, sidecar Seedance reference clips, seven nonessential image refs, final `referenceImages`, and final `referenceVideos`. It keeps the serial Combine/Claude planner/refiner path, generates only `Ref Image 01` and `Ref Image 09`, feeds them into final Seedance `firstFrame`/`lastFrame`, and keeps final Seedance `generateAudio` enabled. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-keyframe-only` passes. Live invocation `f2071527-86b9-4471-81e3-ee769f20f051` crossed the old 72.5% wall and reached 80%, then finished `SUCCEEDED` with no exposed outputs.
- `9c0f1f38-e664-4b9e-9402-f2dae15b692b`: Newly published text-only fallback checkpoint. The graph removes image refs, sidecar audio, sidecar Seedance reference clips, final `referenceImages`, and final `referenceVideos`. It keeps the serial Combine/Claude planner/refiner path, feeds final Seedance only with `TCS Refinement: Claude prompt.text -> textPrompt`, exposes final `video`, and keeps final Seedance `generateAudio` enabled. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults` passes, but live invocation `4732c4b5-f714-48bf-8b8c-a5d0ac5f96d9` finished `SUCCEEDED` with no exposed outputs.
- `f4ed6cf3-69b0-436b-a37c-82e1a7eeeb46`: Current image-board row-1 checkpoint. The graph keeps the stable 13 app inputs, serial Combine chain, Claude planner, JSON parsers for `image_reference_prompts[0..2]`, and three Nano Banana Pro image nodes (`Ref Image 01-03`). It removes final Seedance and sidecar reference clips, and exposes the three image outputs. Direct invocation `d99becc7-1da3-489a-a94e-c1bd4c693621` completed `SUCCEEDED` with 3 image outputs.
- `06a818f1-6dec-4cae-878d-ceeb6fbd5c2d`: Image-board row-2 checkpoint. Same board-only graph shape as row 1, but parses `image_reference_prompts[3..5]`, generates `Ref Image 04-06`, and exposes three image outputs. Direct invocation `f7360924-0e1f-479d-a223-0d53ff901813` completed `SUCCEEDED` with 3 image outputs.
- `fd051825-a295-4406-a80b-1fbfd8f8b7da`: Image-board row-3 checkpoint. Same board-only graph shape as row 1, but parses `image_reference_prompts[6..8]`, generates `Ref Image 07-09`, and exposes three image outputs. Direct invocation `dcfe5d44-e8f7-4bbf-9fdc-0da897b5f0ae` completed `SUCCEEDED` with 3 image outputs.
- `8ab20d96-444e-4751-aa91-9c0b44c5036c`: Nine-image final reference checkpoint published from editor version 267. It keeps the stable 13 app inputs, serial Combine chain, Claude planner/refiner, and all nine Nano Banana image nodes. It removes sidecar audio, motion reference clips, final `firstFrame`, final `lastFrame`, and final `referenceVideos`, then routes the nine image outputs into final Seedance `referenceImages` with indexes `0..8`. Final Seedance `video` and all nine image outputs are exposed in the graph. Live invocation `f030c851-4eea-41ce-b3a3-7a5b3f86658d` finished `SUCCEEDED` with empty output, no failure, and no node-error metadata, so keep this as a diagnostic checkpoint rather than the demo path.
- `2866261a-9e0c-434e-8e32-b41da06ef9d4`: Parser-normalized no-audio checkpoint inspired by Runway's copied `JSON_example` workflow. The graph adds nine concat normalizers between image parser outputs and Gemini prompts, preserves parser `from.index=0` on all image prompt edges, keeps final `referenceImages`, and disables final Seedance `generateAudio`. Invocation `a2c33089-e7f0-48c5-bfaa-e531dff83833` still completed `SUCCEEDED` with empty output and no failure metadata.
- `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33`: Example-driven one-image Gemini-to-Seedance reference diagnostic. After inspecting `Storyboard to Film_example` and `JSON_StoryPanelsEX`, this graph borrows the one-reference-image-per-video-shot structure but keeps Seedance as the video node: it exposes `TCS Ref Image 01`, routes that generated Gemini image into final Seedance `referenceImages[0]`, disables final `generateAudio`, sets duration to 5 seconds, and exposes final `video`. Invocation `53be6385-7dfb-4f89-b0e7-c7e61e393efc` completed `SUCCEEDED` with empty output, narrowing the blocked Workflow path to generated Gemini image outputs feeding Seedance references.
- `a6eea7bd-f8b0-4fcb-bfca-68445d3f65b6`: Raw `curl.exe` Workflow invocation of endpoint `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33`. It completed `SUCCEEDED` with empty output, matching the Python `httpx` invocation and ruling out SDK typed-field drift as the cause of the Workflow empty-output behavior.
- `6ce25c70-8c4e-454b-9816-3c5569aff0f3`: Static asset Seedance reference diagnostic. The graph removes the generated Gemini image node and routes a fixed Runway image asset into final Seedance `referenceImages[0]`. Raw curl invocation `f6f358be-d4b3-44dd-a407-2fd1b06b1228` completed `SUCCEEDED` with empty output, no failure, and no node errors. Treat Seedance `referenceImages` inside published Workflows as unreliable, not only generated-Gemini handoff.
- `b988c359-4afe-4609-875c-e484b410e57d`: Raw `curl.exe` direct Seedance `POST /v1/text_to_video` task with one image reference from the local board. It completed `SUCCEEDED` with one output, proving the exact docs-style curl payload works outside SDK types.
- `ec5e1e70-0406-41e2-9195-08ef5e32f7c4`: Combined reference routing test with one GPT Image 2 node wired from the serial prompt path into final Seedance `firstFrame`, and the sidecar Seedance proof wired into final Seedance `referenceVideos`. Invocation `23af7906-76c5-448f-8884-a6357025d924` reached `RUNNING` with no output and reported `No model variant mapping for app node type: gpt-tidepool-alpha`, proving the GPT Image 2 failure is node metadata/model mapping, not only parallel wiring.
- `8f46769b-92d3-4412-8c96-89d5d4445f25`: Direct Nano Banana Pro / Gemini 3 Pro Image task proof through `POST /v1/text_to_image`. The first `1080:1920` request returned 400 because `gemini_image3_pro` expects model-specific pixel ratios; retrying with portrait `768:1344` completed `SUCCEEDED` with one image output.
- `07d79876-b8df-4d9b-b0e9-07f63f19c357`: Direct Nano Banana Pro proof using max portrait `3072:5504` completed `SUCCEEDED` with one image output, but direct Seedance `promptImage` rejected the raw PNG because the asset exceeded 16 MB.
- `6abcc1e7-81ec-42fc-90e5-b0277e134d3f` -> `83e7205d-7e4f-4f8c-81ad-50b963fc0f66`: Direct Nano Banana Pro at high-resolution portrait `1536:2752` completed, then direct Seedance `POST /v1/image_to_video` accepted it as `promptImage` first frame and completed `SUCCEEDED` with one video output. This is a historical direct first-frame handoff proof.
- `5bf9b443-cdf0-443c-b752-9e292592e69b`: Direct Seedance text-to-video task submitted with the nine proven image-board outputs as `references: [{"uri": image_url}]`. It completed `SUCCEEDED` with one MP4 output.
- Package pages now expose two direct creator-approved lanes: one-image Nano Banana first-frame to Seedance image-to-video, and a dedicated nine-image board lane that submits/checks the three row workflows before submitting Seedance text-to-video with nine image references.
- Extra Runway examples inspected on 2026-05-10: `60398763-9b47-473a-8ca3-066465d39bbc` (`Storyboard to Film_example`) confirms Gemini image chaining and Gemini-image-to-Kling-video handoff with one `referenceImages[0]` image per video node; `e309a30a-364d-4bc0-ae4e-e43db1552c8a` (`JSON_StoryPanelsEX`) confirms Gemini image-panel chaining with varied aspect ratios. Neither example uses Seedance, so they support TCS's one-shot sidecar design but do not prove Workflow Seedance image-reference routing.

Workflow graph target:

1. Primitive Text input nodes for the logical inputs above.
2. Serial Combine Text chain that preserves the explicit input contract while producing one director brief; avoid wide parallel Combine fan-in because endpoint `ff2496e8-f10b-4b2a-a98a-fa474bc0b599` hit Workflow API scheduler errors.
3. Claude director/planner node that returns strict JSON with a final Seedance prompt, image reference briefs, reference-clip motion briefs, and safety reminders.
4. Parse JSON node that fans out the director plan.
5. Nano Banana Pro / Gemini 3 Pro Image (`gemini_image3_pro`) nodes or direct `POST /v1/text_to_image` tasks for a nine-image reference board. Use `1536:2752` for app-side Gen-4.5/Veo prompt-image handoffs, `3072:5504` for max-quality previsuals that will be resized/compressed before video-model handoff, and Nano Banana / Gemini 2.5 Flash (`gemini_2.5_flash`) for fast draft references. Avoid published GPT Image 2 workflow nodes that resolve to `appNodeType: gpt-tidepool-alpha`; those produced `No model variant mapping` errors even when wired serially.
6. Text to SFX sidecar nodes are disabled in the current endpoint. Reintroduce them only if a later Seedance workflow node exposes reliable audio-reference ports or the edit package needs separate SFX assets.
7. Three short reference-clip nodes that group images `1-3`, `4-6`, and `7-9`; fold sound-design direction into each reference-clip prompt while sidecar audio is disabled. The Runway Storyboard-to-Film example uses one generated Gemini image per Kling video node. If TCS stays inside Workflows for reference clips, mimic that one-image-per-shot structure and keep the clips exposed as sidecar outputs for inspection.
8. Final Seedance 2.0 node using portrait `9:16`, 10-12 second duration, 1080p-equivalent app aspect input `1080:1920`, and generated audio enabled only on the stable prompt-only path. Seedance image references should stay in the direct API lane for the hackathon demo because the nine-image endpoint `8ab20d96...`, one-image generated-Gemini endpoint `7ab7c6c7...`, and static-asset endpoint `6ce25c70...` all returned empty Workflow outputs after images were routed into Seedance `referenceImages`.

## Video Model Adapter Plan

Preserve the audience loop, but reshape the creative contract for Gen-4.5 and Veo 3.1:

1. Collect audience signal, creator intent, subject continuity, scene world, motion arc, camera language, audio design, sync notes, duration, aspect, and safety constraints.
2. Build one unified audio-video director packet so motion, camera, and sound are planned together instead of as independent sidecars.
3. Use Gemini / Nano Banana Pro to create the image board from that packet.
4. Send the visual/motion side into Gen-4.5 for silent cinematic shot studies, and send the full audio-video packet into Veo 3.1 for final native-sound generation.
5. Treat image upscaling as an optional pre-video-reference step after Nano Banana Pro images are created and before they are used as video references, but only after a real Precision v2/upscaler API endpoint is confirmed.

Adapter notes:

- Gen-4.5 is the preferred adapter for best-looking silent cinematic shots.
- Veo 3.1 is the preferred adapter for the final video because it supports native audio/sound generation.
- Public `POST /v1/image_to_video` currently supports `gen4.5` and `veo3.1` with one `promptImage`, vertical `720:1280`, and 2-10 second duration.
- Public `POST /v1/text_to_video` currently supports `gen4.5` and `veo3.1` as prompt-only generation with `1280:720` or `720:1280` and 2-10 second duration.
- No public Precision v2 / Magnific upscaler endpoint has been confirmed. Do not invent a model slug; keep that step manual/pending until Runway documents it.

When a custom workflow is created in the Runway app, its API endpoint should appear in the Developer Portal workflow endpoint list for the Techman Studios organization:

- https://dev.runwayml.com/organization/8f8366b8-b7b6-4f9c-baae-f72c16c9f79f/workflows

## High-Value Docs Pages

- Create account / setup: https://docs.dev.runwayml.com/guides/setup/
- Using the API: https://docs.dev.runwayml.com/guides/using-the-api/
- Models: https://docs.dev.runwayml.com/guides/models/
- Pricing: https://docs.dev.runwayml.com/guides/pricing/
- Go-live checklist: https://docs.dev.runwayml.com/guides/go-live/
- API changelog: https://docs.dev.runwayml.com/api-details/api_changelog/
- API versioning overview: https://docs.dev.runwayml.com/api-details/versioning/
- Version 2024-11-06: https://docs.dev.runwayml.com/api-details/versions/2024-11-06/
- Uploading assets: https://docs.dev.runwayml.com/assets/inputs#uploading-assets
- Troubleshooting: https://docs.dev.runwayml.com/errors/troubleshooting/
- Playground: https://dev.runwayml.com/models

## Seedance 2

Seedance notes are retained only for historical diagnostics and older endpoint interpretation. New hackathon app paths should use Gen-4.5 and Veo 3.1.

- Guide: https://docs.dev.runwayml.com/guides/seedance/
- Supports text-to-video, image-to-video, and video-to-video.
- Supports optional image, video, and audio references depending on mode.
- Text-to-video image references use `references: [{"uri": image_url}]` and support up to 9 image references.
- Text-to-video video references use `referenceVideos`, support up to 3 videos, and are limited to 15 seconds total.
- Duration: 5 to 15 seconds.
- Useful vertical ratios include `720:1280`, `834:1112`, `496:864`, and `560:752`.
- Audio references require a prompt; text-to-video audio references also need at least one image or video reference.
- The docs note that curl may be the most reliable test path until SDK types catch up for newer Seedance-specific fields.

## Current API Changelog Notes

- `gemini_image3_pro` / Nano Banana Pro image generation is available via `POST /v1/text_to_image`, with up to 14 reference images and 1K/2K/4K output. Direct API portrait ratios include `768:1344`, `1536:2752`, and `3072:5504`; the app client now uses `1536:2752` as the default portrait board/first-frame image size and keeps `1080:1920` as the logical Shorts aspect. Task `8f46769b-92d3-4412-8c96-89d5d4445f25` proved the direct path with `768:1344`.
- `gemini_2.5_flash` / Nano Banana image generation is available as a faster text/image reference fallback.
- `gpt_image_2` is available via text-to-image, but the current GPT Image 2 Workflow node path is blocked by `gpt-tidepool-alpha` model mapping.
- `gen4.5` is available for high-quality text-to-video and image-to-video; use it for silent cinematic shot studies.
- `veo3.1` and `veo3.1_fast` are available for text-to-video and image-to-video; use `veo3.1` for final videos that need native sound.
- ElevenLabs text-to-speech, sound effects, voice isolation, dubbing, and speech-to-speech are available through the API.
- Google Veo 3.1 is available.
- Third-party models include Veo3 and Gemini image models.
- Runway API MCP server is available at https://github.com/runwayml/runway-api-mcp-server.

## Model Swap Methodology

Keep the audience-in-the-loop mechanic as the stable creative contract, not the old Seedance-oriented field count. The app should collect the audience comment, safety interpretation, creator notes, prior-video context, subject continuity, scene world, motion/camera direction, audio design, duration, aspect, and safety constraints, then turn that into one audio-video director packet.

Current demo lane:

1. Use Nano Banana Pro / Gemini 3 Pro Image for the nine-image board.
2. Generate the nine-image board with Gemini / Nano Banana Pro as a separate, inspectable asset lane.
3. Submit the final sound-enabled video through Veo 3.1 image-to-video using one hero board image as `promptImage` and the AV director packet plus nine-board plan in the prompt.

Video adapters:

1. Gen-4.5 adapter: map the visual anchor, subject continuity, motion arc, and camera language into Gen-4.5 image-to-video for silent cinematic shots.
2. Veo 3.1 adapter: map the full AV packet into Veo 3.1 image-to-video for the final sound-enabled video, keeping audio cues locked to visible causes.
3. Seedance adapter: retained only as historical diagnostic context; do not use it for the active hackathon workflow.

Upscaling stage:

- Treat upscaling as a pre-video-reference image step after Nano Banana Pro image generation, not part of the core creative contract.
- Prefer Runway's upscaler if a public API model/workflow slug is confirmed in the Developer Portal.
- If Magnific Precision v2 remains UI-only or has no documented public slug, keep it as a manual/optional polish pass and consider a separate programmatic upscaler only after licensing and quality checks.

Validation rules:

- Every adapter must run the same canonical AV director packet so outputs can be compared fairly.
- Record the selected model slug, endpoint type, reference input shape, duration, ratio, upscaler slug, and sanitized task/invocation IDs.
- Do not replace the demo path until the candidate adapter returns a visible MP4 and survives a small visual QA pass.

## Characters / Avatar Docs

- Characters overview: https://docs.dev.runwayml.com/characters/
- Quickstart: https://docs.dev.runwayml.com/characters/quickstart/
- Custom avatars: https://docs.dev.runwayml.com/characters/create-your-own/
- Core concepts: https://docs.dev.runwayml.com/characters/concepts/
- Building integration: https://docs.dev.runwayml.com/characters/integration/
- Embedded widget: https://docs.dev.runwayml.com/characters/widget/
- Knowledge base: https://docs.dev.runwayml.com/characters/documents/
- Custom voices: https://docs.dev.runwayml.com/characters/custom-voice/
- Client tools: https://docs.dev.runwayml.com/characters/tools/client-tools/
- Server tools: https://docs.dev.runwayml.com/characters/tools/server-tools/
- Tools best practices: https://docs.dev.runwayml.com/characters/tools/best-practices/
- Tools reference: https://docs.dev.runwayml.com/characters/tools/reference/
- Video meeting: https://docs.dev.runwayml.com/characters/video-meeting/
- Camera and screen sharing: https://docs.dev.runwayml.com/characters/screens/
- LiveKit Agents: https://docs.dev.runwayml.com/characters/livekit/
- Troubleshooting: https://docs.dev.runwayml.com/characters/troubleshooting/

## Runway GitHub Organization

Organization: https://github.com/runwayml

The org page reported 61 public repositories. The most relevant for this project are:

- https://github.com/runwayml/sdk-python - Python SDK.
- https://github.com/runwayml/sdk-node - Node/TypeScript SDK.
- https://github.com/runwayml/openapi - Runway API OpenAPI spec.
- https://github.com/runwayml/skills - agent skills for generation and integration.
- https://github.com/runwayml/runway-api-mcp-server - MCP server for Runway generation workflows.
- https://github.com/runwayml/avatars-sdk-react - React SDK for real-time AI avatar interactions.
- https://github.com/runwayml/avatars-node-rpc - Node backend RPC tools for avatar sessions.
- https://github.com/runwayml/runway-studio-skills - Runway Studio agent skills.
- https://github.com/runwayml/runway-characters-meet - example characters meeting app.
- https://github.com/runwayml/live-avatar.github.io - live avatar API docs.

## Full Public Repo Inventory

| Repo | Language | Archived | Notes |
|---|---:|---:|---|
| [livekit-agents](https://github.com/runwayml/livekit-agents) | Python | no | Realtime voice AI agents fork. |
| [runway-pipecat](https://github.com/runwayml/runway-pipecat) | Python | no | Voice and multimodal conversational AI fork. |
| [avatars-sdk-react](https://github.com/runwayml/avatars-sdk-react) | TypeScript | no | React SDK for GWM-1 avatars. |
| [sdk-python](https://github.com/runwayml/sdk-python) | Python | no | Runway Python SDK. |
| [sdk-node](https://github.com/runwayml/sdk-node) | TypeScript | no | Runway Node SDK. |
| [openapi](https://github.com/runwayml/openapi) | Shell | no | Runway API OpenAPI spec. |
| [confingy](https://github.com/runwayml/confingy) | Python | no | Configuration helper. |
| [runway-agents-js](https://github.com/runwayml/runway-agents-js) | TypeScript | no | Realtime multimodal AI agents with Node.js. |
| [runway-characters-meet](https://github.com/runwayml/runway-characters-meet) | HTML | no | Characters meeting example. |
| [runway-api-mcp-server](https://github.com/runwayml/runway-api-mcp-server) | TypeScript | no | Runway MCP server. |
| [skills](https://github.com/runwayml/skills) | Python | no | Runway coding agent skills. |
| [runway-studio-skills](https://github.com/runwayml/runway-studio-skills) | Python | no | Runway Studio skills. |
| [avatars-node-rpc](https://github.com/runwayml/avatars-node-rpc) | TypeScript | no | Backend RPC handler for avatar sessions. |
| [openclaw-skills](https://github.com/runwayml/openclaw-skills) | TypeScript | no | Openclaw skills. |
| [runway-characters-meeting-skill](https://github.com/runwayml/runway-characters-meeting-skill) | Python | no | Characters meeting skill. |
| [openclaw-skill-send-video-message](https://github.com/runwayml/openclaw-skill-send-video-message) | Python | no | Send-video-message Openclaw skill. |
| [live-avatar.github.io](https://github.com/runwayml/live-avatar.github.io) | HTML | no | Live avatar API documentation. |
| [hair-makeover-api-demo](https://github.com/runwayml/hair-makeover-api-demo) | TypeScript | no | API demo. |
| [figma-plugin](https://github.com/runwayml/figma-plugin) | HTML | no | Figma plugin. |
| [terraform-retool-modules](https://github.com/runwayml/terraform-retool-modules) | HCL | no | Terraform modules. |
| [try-on-chrome-extension](https://github.com/runwayml/try-on-chrome-extension) | JavaScript | no | Chrome extension. |
| [chrome-extension-tutorial](https://github.com/runwayml/chrome-extension-tutorial) | JavaScript | no | Chrome extension tutorial. |
| [terraform-aws-wandb](https://github.com/runwayml/terraform-aws-wandb) | HCL | no | Terraform module for Weights & Biases. |
| [fuse-device-plugin](https://github.com/runwayml/fuse-device-plugin) | Go | no | Kubernetes FUSE device plugin. |
| [RunwayML-for-Photoshop](https://github.com/runwayml/RunwayML-for-Photoshop) | TypeScript | yes | Photoshop integration. |
| [learn](https://github.com/runwayml/learn) | unknown | yes | Legacy tutorials and examples. |
| [maxmsp](https://github.com/runwayml/maxmsp) | Max | yes | Max/MSP integration. |
| [k8s-cloudwatch-adapter](https://github.com/runwayml/k8s-cloudwatch-adapter) | Go | no | Kubernetes CloudWatch adapter. |
| [awssecret2env](https://github.com/runwayml/awssecret2env) | Go | no | AWS Secrets Manager to env utility. |
| [circleci-gcp-oidc-terraform](https://github.com/runwayml/circleci-gcp-oidc-terraform) | HCL | no | CircleCI OIDC Terraform. |
| [react-hls](https://github.com/runwayml/react-hls) | TypeScript | no | HLS/RTMP React component. |
| [guided-inpainting](https://github.com/runwayml/guided-inpainting) | Python | no | Keyframe propagation models. |
| [amazon-guardduty-to-slack](https://github.com/runwayml/amazon-guardduty-to-slack) | unknown | no | GuardDuty Slack integration. |
| [hosted-models](https://github.com/runwayml/hosted-models) | TypeScript | yes | Legacy hosted model examples. |
| [model-template](https://github.com/runwayml/model-template) | Python | yes | Legacy model template. |
| [model-sdk](https://github.com/runwayml/model-sdk) | Python | yes | Legacy model SDK. |
| [CHANGELOG](https://github.com/runwayml/CHANGELOG) | unknown | no | Runway app changelog. |
| [ofxRunway](https://github.com/runwayml/ofxRunway) | Makefile | yes | openFrameworks integration. |
| [openh264](https://github.com/runwayml/openh264) | C++ | no | OpenH264 codec. |
| [taxjar-node](https://github.com/runwayml/taxjar-node) | JavaScript | yes | Sales tax API client. |
| [terraform-aws-wireguard](https://github.com/runwayml/terraform-aws-wireguard) | HCL | no | AWS WireGuard Terraform module. |
| [terraform-aws-eks](https://github.com/runwayml/terraform-aws-eks) | HCL | no | AWS EKS Terraform module. |
| [RunwayML-for-Grasshopper](https://github.com/runwayml/RunwayML-for-Grasshopper) | C# | yes | Grasshopper integration. |
| [processing-library](https://github.com/runwayml/processing-library) | Java | yes | Processing library. |
| [touchDesigner](https://github.com/runwayml/touchDesigner) | unknown | yes | TouchDesigner integration. |
| [p5js](https://github.com/runwayml/p5js) | JavaScript | yes | p5.js integration. |
| [Intro-Synthetic-Media](https://github.com/runwayml/Intro-Synthetic-Media) | JavaScript | no | Synthetic media class materials. |
| [model-face-recognition](https://github.com/runwayml/model-face-recognition) | Python | yes | Legacy face recognition model. |
| [design](https://github.com/runwayml/design) | unknown | no | Design resources. |
| [puredata](https://github.com/runwayml/puredata) | unknown | yes | Pure Data integration. |
| [OpenRNDR](https://github.com/runwayml/OpenRNDR) | Kotlin | yes | OpenRNDR integration. |
| [javascript](https://github.com/runwayml/javascript) | JavaScript | yes | Legacy JavaScript integration. |
| [arduino](https://github.com/runwayml/arduino) | C++ | yes | Arduino integration. |
| [processing](https://github.com/runwayml/processing) | Processing | yes | Archived Processing integration. |
| [RunwayML-for-Unity](https://github.com/runwayml/RunwayML-for-Unity) | C# | yes | Unity integration. |
| [unity](https://github.com/runwayml/unity) | C# | yes | Archived Unity integration. |
| [Arbitrary-Image-Stylization](https://github.com/runwayml/Arbitrary-Image-Stylization) | Python | yes | Legacy model. |
| [model-squeezenet](https://github.com/runwayml/model-squeezenet) | Python | yes | Legacy SqueezeNet model. |
| [alpha_models](https://github.com/runwayml/alpha_models) | PureBasic | yes | Alpha models. |
| [runway](https://github.com/runwayml/runway) | unknown | yes | Deprecated alpha app. |
| [alpha_website](https://github.com/runwayml/alpha_website) | JavaScript | yes | Alpha website. |

## Runway Skills Repo Notes

- Install skills for compatible agents with `npx skills add runwayml/skills`.
- Generation skills: `rw-generate-video`, `rw-generate-image`, `rw-generate-audio`.
- Integration skills: `rw-integrate-video`, `rw-integrate-image`, `rw-integrate-audio`.
- Setup/reference skills: `rw-recipe-full-setup`, `rw-check-compatibility`, `rw-setup-api-key`, `rw-check-org-details`, `rw-api-reference`, `rw-fetch-api-reference`.
- Utilities: `use-runway-api`, `rw-integrate-uploads`.

## Recommendation For Top Comment Studio

Start with server-side Runway calls only. Keep `RUNWAYML_API_SECRET` off the client, generate vertical Shorts prompts by default, and use manual approval before spending credits on video generation.
