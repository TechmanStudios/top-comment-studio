# Known Issues

Track setup blockers, bugs, and limitations here.

## Template

```text
Issue:
Impact:
Reproduction:
Current workaround:
Owner:
Status:
```

---

## Current Issues

### Precision v2 Upscaler API Not Confirmed

Issue: Public Runway docs inspected for the Gen-4.5/Veo pivot did not expose a Precision v2, Magnific, or equivalent upscaler endpoint/model slug.
Impact: The app cannot safely automate the requested post-Nano-Banana/pre-video-reference upscaling step without inventing an unsupported API payload.
Reproduction: Review the current Runway public API docs and model catalog for text/image/video endpoints and upscaler model slugs.
Current workaround: Keep upscaling manual/pending. Only add automated upscaling after Runway documents the endpoint, then run it after Nano Banana Pro image generation and before Gen-4.5/Veo image-to-video handoff.
Owner: Bryan / project team.
Status: open

### All-In-One Image-Reference Workflow Returns Empty Output

Issue: Published endpoint `8ab20d96-444e-4751-aa91-9c0b44c5036c` routes all nine Nano Banana image outputs into final Seedance `referenceImages`, with final `firstFrame`, `lastFrame`, and `referenceVideos` removed, but live invocation `f030c851-4eea-41ce-b3a3-7a5b3f86658d` finished `SUCCEEDED` with an empty output object and no failure or node-error metadata. Endpoint `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33` narrowed the repro further by routing only one generated Gemini image into Seedance `referenceImages[0]`; invocation `53be6385-7dfb-4f89-b0e7-c7e61e393efc` also finished `SUCCEEDED` with empty output. Raw `curl.exe` invocation of that same endpoint reproduced the result as invocation `a6eea7bd-f8b0-4fcb-bfca-68445d3f65b6`, also `SUCCEEDED` with empty output. Static asset endpoint `6ce25c70-8c4e-454b-9816-3c5569aff0f3` removed the Gemini image node and routed a fixed Runway image asset into Seedance `referenceImages[0]`; invocation `f6f358be-d4b3-44dd-a407-2fd1b06b1228` also completed `SUCCEEDED` with empty output, no failure, and no node errors.
Impact: Seedance `referenceImages` inside published Workflows are not reliable for the hackathon demo yet, even though the equivalent direct Seedance text-to-video image-reference API path works.
Reproduction: Invoke endpoint `8ab20d96-444e-4751-aa91-9c0b44c5036c` with the standard 13 app inputs and inspect invocation `f030c851-4eea-41ce-b3a3-7a5b3f86658d`, invoke one-image diagnostic endpoint `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33` and inspect invocation `53be6385-7dfb-4f89-b0e7-c7e61e393efc`, or invoke static asset endpoint `6ce25c70-8c4e-454b-9816-3c5569aff0f3` and inspect invocation `f6f358be-d4b3-44dd-a407-2fd1b06b1228`.
Current workaround: Use the package-page image-board lane: generate/check the three row workflows, then submit the final video through Veo 3.1 image-to-video with one hero board image as `promptImage` and the unified AV director packet plus nine-board plan compressed into the prompt. Task `5bf9b443-cdf0-443c-b752-9e292592e69b` remains a historical direct Seedance proof, but it is no longer the current hackathon app path. Parser-normalized endpoint `2866261a-9e0c-434e-8e32-b41da06ef9d4`, based on the copied `JSON_example` parser/concat pattern and final `generateAudio=false`, also returned `SUCCEEDED` with empty output, so this is not only a parser-socket, reference-count, generated-audio, generated-Gemini handoff, or Python SDK issue. Further paid work should pivot to Gen-4.5, Veo 3.1, and confirmed upscaler adapter tests rather than more Seedance `referenceImages` Workflow shapes.
Owner: Bryan / project team.
Status: open

### Earlier Runway V1.1 Endpoints Returned No Final Video

Issue: Published endpoints `8ae9c852-4319-417c-9d08-f389570b5db1`, `4cec124c-3217-4435-844c-0b794dc2cdcc`, and wide parallel Combine endpoint `ff2496e8-f10b-4b2a-a98a-fa474bc0b599` accepted the app payload but completed with empty outputs. The GPT Image 2 endpoints failed on `gpt-tidepool-alpha`; the wide Combine endpoint reported `Node is already running in this execution` on Combine nodes.
Impact: The app can submit live Runway jobs, the serial text-only rich endpoint returns video, one sidecar Seedance reference-clip node can return video, direct Nano Banana Pro image generation is proven, and direct Nano Banana-to-Seedance first-frame handoff is proven. Workflow image-node routing and final-Seedance video-reference routing still need tiny endpoint proofs before joining the final published workflow path.
Reproduction: Inspect invocation `8b5d57dd-7469-4b19-b572-3cc732237110` on the GPT Image endpoint, `070080f5-6c2e-4724-bb02-9ca9a9a97d61` on the parsed text-only endpoint, or `1eb5bf3b-ef8d-4c21-9968-9dd77eecb545` on the wide parallel Combine endpoint.
Current workaround: Use sidecar reference proof endpoint `b9beb013-0fe5-4f20-b244-a39b788ae95d`, where all 13 app inputs feed a serial Combine chain, planner Claude, Parse JSON, refiner Claude, final Seedance, and one sidecar Seedance proof node. Invocation `06ee71a5-3e6e-4b36-ade3-7d199bada83a` returned two Seedance MP4 URLs with zero node errors.
Owner: Bryan / project team.
Status: resolved for text-only rich workflow, independent sidecar Seedance reference clip, direct Nano Banana Pro image generation, and direct Seedance first-frame handoff; open for Workflow image-node routing and final video-reference routing

### Manual Canvas Runs Can Succeed While Workflow API Outputs Stay Empty

Issue: Bryan manually clicked Run on the Seedance node fed by the JSON parser and the canvas produced a video after about three minutes, but published Workflow API invocations have not yet returned a usable output URL from the fuller graph.
Impact: The creative canvas graph can generate video, and published API checkpoints now work through the serial text-only rich stage plus one independent sidecar Seedance reference clip. Direct Nano Banana Pro image generation works, and direct Seedance image-to-video can use a `1536:2752` Nano Banana output as the first frame. Final `referenceVideos` routing and Workflow image-node routing still need separate published proofs.
Reproduction: Compare the successful manual Seedance canvas run with earlier published invocations `070080f5-6c2e-4724-bb02-9ca9a9a97d61` and `e46ba302-ccde-4ff8-97fb-796b13e6de15`, then compare the proven minimal invocation `ba15f8c4-8363-4a6d-b16f-a117daf3b605` and serial rich invocation `de9c70e6-972a-44ca-ae16-119d3d1ab762`.
Current workaround: Rebuild the richer workflow only from published endpoint states that prove output exposure. The current safe base is `b9beb013-0fe5-4f20-b244-a39b788ae95d`.
Owner: Bryan / project team.
Status: resolved for minimal Seedance, serial text-only rich workflow, one independent sidecar Seedance reference clip, direct Nano Banana Pro image generation, and direct Seedance first-frame handoff; open for Workflow image-node routing and final video-reference routing

### Disconnected Workflow Nodes Still Execute Through Workflow API

Issue: Endpoint `45745fae-baed-498c-b84e-84c9ff5549bb` had only one visible edge from `TCS Input: script` to Seedance, but disconnected nodes remained on the canvas. Workflow API invocation `4290417d-7633-457f-8651-6de272fc3a69` still executed the disconnected Claude node and reported `Invalid task options: prompt: Invalid input: expected string, received undefined`.
Impact: Hiding or disconnecting nodes is not enough for published API diagnostics; unused model nodes must be deleted or fully configured.
Reproduction: Inspect endpoint `45745fae-baed-498c-b84e-84c9ff5549bb` and invocation `4290417d-7633-457f-8651-6de272fc3a69`.
Current workaround: Keep only the nodes intended to run in the published endpoint. For the active minimal repro, use endpoint `5d1d6d5f-c194-4aaf-841a-bf68fa618425`.
Owner: Bryan / project team.
Status: open

### GPT Image 2 Workflow Node Metadata Is Mixed

Issue: A freshly added `GPT Image 2 Text/Image to Image` workflow node can generate successfully when Bryan manually clicks Run in the Runway canvas, and it publishes with `taskType: workflow_gpt_image_2`, but it still reports `appNodeType: gpt-tidepool-alpha`.
Impact: GPT Image 2 works in the Runway backend/manual canvas path, but the current published workflow endpoint still fails with `No model variant mapping for app node type: gpt-tidepool-alpha`, so explicit search selection alone is not enough for Workflows API execution.
Reproduction: Inspect endpoint `8ae9c852-4319-417c-9d08-f389570b5db1` through `GET /v1/workflows/{id}` and review node `ba321c8f-59a2-44a0-8901-1945968f7b49`. Endpoint `ec5e1e70-0406-41e2-9195-08ef5e32f7c4`, invocation `23af7906-76c5-448f-8884-a6357025d924`, reproduced the same error after wiring one GPT Image 2 node serially into final Seedance `firstFrame`.
Current workaround: Avoid routing GPT Image 2 workflow-node outputs into the final video branch. For hackathon image references, use Nano Banana Pro / Gemini 3 Pro Image (`gemini_image3_pro`) through `POST /v1/text_to_image`, with Nano Banana / Gemini 2.5 Flash (`gemini_2.5_flash`) as the fast fallback. Use the board's first hero image as the Gen-4.5/Veo prompt image; max `3072:5504` PNG outputs may need resizing/compression before video-model handoff.
Owner: Bryan / project team.
Status: open

## Resolved Issues

### Runway Workflow Endpoint Not Published Yet

Issue: The app had a creator-approved submit route, but live Runway generation was blocked until `TCS Seedance Director v1` was published and its node map was captured.
Impact: Resolved. The workflow endpoint is published and the node map is documented.
Reproduction: Open the Runway Developer Portal workflow endpoint list.
Current workaround: None needed for publishing; local `.env` still needs configuration.
Owner: Bryan / project team.
Status: resolved

### GitHub Repo Creation Permission

Issue: The available GitHub CLI token cannot create `TechmanStudios/top-comment-studio`.
Impact: Resolved. The repository now exists publicly at `https://github.com/TechmanStudios/top-comment-studio`.
Reproduction: Run `gh repo create TechmanStudios/top-comment-studio --public --description 'Audience-in-the-loop YouTube Shorts workflow powered by Runway API.'`.
Current workaround: None needed.
Owner: Bryan / TechmanStudios admin.
Status: resolved
