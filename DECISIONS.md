# Decision Log

Record important technical and product decisions here.

## Format

```text
Date:
Decision:
Why:
Alternatives considered:
Tradeoffs:
Follow-up:
```

---

## Decisions

### 2026-05-11 — One-Click Judge Render Flow

Decision: Treat the intake page's `Generate render` button as the only visible judge-facing paid action. It creates the episode package, submits the configured v66 workflow with locked defaults, and sends the user to the render monitor page.

Why: The demo needs one clear action from audience signal to video render. Earlier two-step approval/package flows and package-page diagnostic lanes added confusion and exposed unproven variants.

Alternatives considered: Keep a separate package page approval button, expose the image-board/direct-generation lanes, or make Director Controls editable for live prompt variation.

Tradeoffs: The public flow is simpler and safer, but it hides some internal package/debug detail that remains useful for future engineering work.

Follow-up: Keep the one-click flow for final submission. Reintroduce advanced controls or asset lanes only behind an admin/debug surface after paid smoke tests prove those variants return MP4 outputs.

### 2026-05-11 — Lock Director Controls For Competition Demo

Decision: Keep the Director Controls section visible on the intake page, but make its fields read-only and ignore posted Director Control values in the public `/package` route.

Why: A customized Director Controls test produced a Runway completion with no exposed workflow output. The competition path should keep the audience comment editable while preserving the paid-proven v66 prompt defaults.

Alternatives considered: Remove the section entirely, keep the fields editable and rely on the user to avoid risky edits, or rebuild the Runway workflow around every control variant.

Tradeoffs: The judge-facing flow is safer and simpler, but quick creative customization from the homepage is paused. Programmatic/package API paths can still create `CommentInput` records with custom controls for internal tests and future workflow work.

Follow-up: Re-enable editable controls only after a small set of custom prompt variants completes paid smoke tests with exposed MP4 outputs.

### 2026-05-11 — Use Render Subdomain For Judging

Decision: Use `https://top-comment-studio.onrender.com/` as the active judge URL for now, leaving `top-comment.techmanstudios.com` as a deferred polish item.

Why: The Render subdomain is already live, HTTPS-enabled, and validates the real server-side Runway flow without waiting on DreamHost DNS propagation.

Alternatives considered: Finish the Techman Studios custom subdomain before submitting the judging link.

Tradeoffs: The onrender.com URL is less branded, but it reduces setup risk and keeps the demo path simple. The custom domain can still point at the same service later.

Follow-up: If brand polish becomes important after judging, add the DreamHost `CNAME` host `top-comment` to target `top-comment-studio.onrender.com`, then verify the domain in Render.

### 2026-05-11 — Live Demo Requires Server-Backed Hosting

Decision: Use a server-backed Python or Docker host for the live judging URL, optionally behind a Techman Studios subdomain, instead of trying to run the app from GitHub Pages.

Why: GitHub Pages only serves static files and cannot run FastAPI or protect the Runway API secret. The app's one-click render flow must keep Runway credentials on the server while exposing a public URL to judges.

Alternatives considered: GitHub Pages static hosting, DreamHost shared hosting, a DreamHost VPS, or a managed app host such as Render, Railway, Fly.io, or DigitalOcean App Platform.

Tradeoffs: A server-backed host adds deployment setup and runtime cost, but it preserves the current working app behavior and keeps secrets out of the public repo. GitHub Pages can still be used later for a static project/README site, but not for paid generation.

Follow-up: Deploy with the root `Dockerfile` or the documented `uvicorn` start command, set secrets in the host dashboard, attach persistent storage if available, and point `top-comment.techmanstudios.com` or another subdomain at the host.

### 2026-05-11 — Package Generation Can Start v66 Workflow

Decision: Let the intake form submit the current v66 Runway workflow during `Generate package` when the creator-approved checkbox is checked, while keeping the existing package-page submit route as a manual fallback.

Why: Bryan wants the app flow to continue from comment package generation into rendered video generation without making a second page feel like the real starting point. The workflow still spends Runway credits, so the creator approval gate remains explicit.

Alternatives considered: Auto-submit on every package generation without approval, or leave workflow submission only on the package page.

Tradeoffs: One checkbox keeps the paid-generation boundary visible, but the happy path is now a single generate action. The package page auto-refreshes the status endpoint until the workflow returns an MP4.

Follow-up: During demo rehearsal, use a safe prompt and confirm the `Open rendered video` action updates from the v66 workflow output after Runway returns `final_storyboard_short_16s`.

### 2026-05-11 — Techman-Themed App Shell

Decision: Keep the MVP as a server-rendered FastAPI/Jinja app and restyle the existing templates around the Techman Studios public-site theme: dark cinematic canvas, ivory block typography, gold primary actions, blue-green grid/circuit atmosphere, and compact uppercase navigation.

Why: The workflow engineering is at a demo checkpoint, and the next useful move is improving the app experience without adding a frontend build system or changing the proven Runway contract.

Alternatives considered: Build a React/Next.js frontend, copy website assets directly, or leave the plain scaffold until more app features exist.

Tradeoffs: A CSS/Jinja pass is less flexible than a component frontend, but it is faster, reviewable, and keeps the hackathon app easy to run. The design echoes the website without depending on external brand images.

Follow-up: After the core demo flow is stable, consider extracting a shared base template and adding lightweight client-side enhancements for package review and Runway status refresh.

### 2026-05-10 — 1080p Seamless-Keyframe Demo Checkpoint

Decision: Publish a version 66 checkpoint that keeps the seamless-keyframe Continuity Core design, sets all Veo 3.1 segments to `1080p`, and spaces the generated-frame/enhancer/video rows for clearer Runway editor inspection.

Why: Version 63 proved the keyframe transition design, but its paid output was 720x1280. The demo target needs 1080x1920 output, and the added transition wiring made the canvas harder to inspect without a small layout cleanup.

Alternatives considered: Keep version 63 as the demo checkpoint, upscale the final MP4 outside Runway, or use the intermediate version 65 endpoint. Native 1080p generation is cleaner than post-upscaling, and version 65 was rejected because the published Developer API graph dropped input labels and the exposed final output.

Tradeoffs: Version 66 likely costs and runs heavier than version 63 because every Veo segment renders at 1080p. Static validation and one paid smoke succeeded, but rehearsal timing should be watched.

Follow-up: Use endpoint `c1b49d17-c80f-4705-b0e6-86c89a070464` as the current 1080p demo checkpoint, and keep version 63 endpoint `65e09485-4169-41d9-9282-85b52148949f` as the paid-proven 720p fallback.

### 2026-05-10 — Seamless-Keyframe Continuity Checkpoint

Decision: Publish a version 63 checkpoint that keeps the version 62 Photo Enhancer chains, adds Story Panels-inspired continuity guidance, and routes adjacent enhanced frames into Veo 3.1 `endFrame` inputs so each segment lands on the next storyboard panel.

Why: Version 62 was paid-proven, but the final stitched short could still read like four separate generated clips. Runway featured workflow `529` showed useful story-panel continuity language, and featured workflow `364` showed the practical Veo `startFrame` plus `endFrame` pattern for smoother transitions.

Alternatives considered: Keep version 62 unchanged, add separate transition clips between the four segments, or replace the four-segment structure with a single longer video node. The single-node path is unproven for this Workflow contract, and extra transition clips would increase length/cost while complicating the app's existing 16-second output.

Tradeoffs: Version 63 keeps the same node count and generation-cost profile as version 62 but adds three more image-to-video edges and uses `workflow-veo3-1-keyframes-task` for the first three Veo nodes. Static validation and one paid smoke succeeded, but keyframe behavior should still be watched during demo rehearsals.

Follow-up: Use endpoint `65e09485-4169-41d9-9282-85b52148949f` as the current seamless-keyframe demo checkpoint, and keep version 62 endpoint `277aecec-43a4-4042-844e-e9e3d41db8d3` as the paid-proven photo-enhanced fallback.

### 2026-05-10 — Photo-Enhanced Continuity Checkpoint

Decision: Publish a version 62 checkpoint that routes each Gemini storyboard frame through the Runway featured workflow `596` Photo Enhancer method before the frame reaches its Veo 3.1 `startFrame` segment input.

Why: Version 59 is paid-proven, but Veo's final native-audio segments can benefit from cleaner, more cinematic start frames. Placing enhancement inside the existing Continuity Core preserves the Audience-in-the-Loop planning path and keeps the final stitch output unchanged.

Alternatives considered: Keep version 59 unchanged, add a single fixed-prompt Gemini image pass instead of the full featured method, or run enhancement as a separate app-side/manual step after workflow generation.

Tradeoffs: Version 62 adds 16 Gemini API calls and 8 Gemini Image Pro calls per full invocation, so it is more expensive than version 59. Version 61 also showed that static validation is not enough for Gemini API node runtime names: `appNodeType: gemini-api` published but failed at runtime, while version 62 uses `appNodeType: gemini`.

Follow-up: Use endpoint `277aecec-43a4-4042-844e-e9e3d41db8d3` as the current photo-enhanced demo checkpoint, and keep version 59 documented as the cheaper paid-proven fallback.

### 2026-05-10 — Continuity Core Outer Planning Ring

Decision: Treat the paid-proven Storyboard-to-Short graph as the `Continuity Core` and connect the TCS Director and TCS Asset Planner back into it as upstream text-planning nodes, not as a separate media branch stitched into the final output.

Why: Version 56 proved the continuity spine with one anchor, sequential frames, Veo 3.1 `startFrame` segments, and one final stitch. The older final-master branch proved the director/asset planner ideas were useful, but its independent media branch weakened visual continuity.

Alternatives considered: Reconnect the old 4-second director preview and full asset-media branch into the final stitch, or keep the version 56 storyboard core without the richer director/asset planner context.

Tradeoffs: Version 57 adds two Claude planning nodes and one parser before generation, so it may cost more than version 56 at invocation time, but it avoids the much larger cost and continuity risk of generating a separate board/sidecar/segment branch outside the core spine.

Follow-up: Run a paid smoke only after Bryan approves the spend, then compare the contact sheet against version 56 for first-frame subject readability and continuity.

### 2026-05-10 — Parsed Asset Planner Into Continuity Core

Decision: Route `TCS Asset Parser: boards sidecars segments` into a new `TCS Asset Planner: parsed creative map` node, then feed that parsed map into the Continuity Core instead of sending only the Asset Planner's raw JSON.

Why: The raw Asset Planner Claude output was already upstream, but the parser node was visually and structurally dangling. Feeding the parsed board, sidecar, segment, and continuity-note outputs makes the Asset Planner part of the final creative prompt path and gives the Continuity Core cleaner shot intelligence.

Alternatives considered: Leave the parser as a diagnostic dead-end, feed the raw Asset Planner JSON directly, or generate the old independent board/sidecar media branch again.

Tradeoffs: Version 59 adds one concat node and more parser edges, which makes the graph busier, but it avoids the credit cost and continuity risk of a separate generated media branch.

Follow-up: Run a paid smoke only after Bryan approves the spend, then compare against version 57's contact sheet.

### YYYY-MM-DD — Initial Repo Setup

Decision: Use lightweight repo-level AI instructions and setup templates.

Why: Hackathon work needs fast onboarding and consistent agent behavior.

Alternatives considered: Heavy process docs or no shared guidance.

Tradeoffs: Some templates are placeholders until the exact stack is confirmed.

Follow-up: Replace placeholders as the implementation becomes clear.

### 2026-05-09 — Project Name and Public Repo Target

Decision: Use `Top Comment Studio` as the project name and `top-comment-studio` as the GitHub repository slug.

Why: The name directly reflects the MVP mechanic: using the selected top audience comment as the creative seed for the next Short.

Alternatives considered: Keeping the working `aiYoutube` or `runwayHackathon` names.

Tradeoffs: The new name is product-oriented, while the folder name still reflects the original hackathon scaffold.

Follow-up: Rename the local folder later if desired after the public repo is created.

### 2026-05-09 — Secret Handling

Decision: Store the real Runway API secret only in local `.env`; prefer `RUNWAYML_HACKATHON_API_SECRET` for hackathon calls and keep `.env.example` placeholder-only.

Why: The project is being prepared for a public repository and must not publish live credentials. Bryan deleted the old Runway API key, leaving the hackathon key as the only active key in the portal.

Alternatives considered: Leaving the old `RUNWAYML_API_SECRET` variable available as a fallback.

Tradeoffs: Contributors must copy or request the real hackathon secret locally, but the repo remains safe to publish and local API usage is easier to attribute to the hackathon key.

Follow-up: Keep `RUNWAYML_API_SECRET` out of local `.env` unless a non-hackathon fallback is intentionally restored.

### 2026-05-09 — Local Browser Session Exports

Decision: Ignore local browser cookie, login, session, auth-state, and storage-state exports at the repo level.

Why: Runway app and Developer Portal sessions may be useful for local workflow setup, but they must never be uploaded to the public repository.

Alternatives considered: Relying only on local `.git/info/exclude`.

Tradeoffs: Broad filename patterns may ignore future local files with session/cookie/auth naming, which is acceptable for safety.

Follow-up: Keep durable, non-secret workflow notes in docs instead of exporting account state into tracked files.

### 2026-05-09 — Runway Workflow Endpoint Registry

Decision: Track custom Runway Workflow endpoints through the Techman Studios Developer Portal workflow list.

Why: Custom workflows created in the Runway app expose their API endpoints under the organization workflow endpoint page, which is the source of truth for integration work.

Alternatives considered: Keeping endpoint URLs only in browser history or chat notes.

Tradeoffs: The organization ID is now documented, but no secrets or session cookies are included.

Follow-up: Document each created workflow's input schema, output schema, and endpoint name once available.

### 2026-05-09 — First MVP Implementation Stack

Decision: Use Python 3.12+, FastAPI, Jinja templates, local JSON storage, pytest, and `uv` for the first runnable MVP scaffold.

Why: The repo guidance prefers Python for new scaffolds, and this stack keeps the hackathon demo simple, inspectable, and server-side safe for Runway API calls.

Alternatives considered: Next.js full-stack app, separate React frontend with Python API, or CLI-only prototype.

Tradeoffs: A server-rendered UI is less flashy than a full SPA, but it gets the audience-comment-to-package loop running faster with fewer moving pieces.

Follow-up: Add the scaffold and real commands in the next phase, then update README once `uv sync`, dev, and test commands exist.

### 2026-05-09 — First Workflow Model Stack

Decision: Use GPT 5.5 for LLM text generation, OpenAI Images 2.0 for image generation, and Seedance 2.0 for video generation in the first custom Runway workflow design.

Why: This stack matches Bryan's preferred workflow direction and keeps the first integration focused on text-to-visual-to-video production.

Alternatives considered: Gen-4.5 video, Gen-4 Image/Turbo, Gemini image models, and Veo 3/3.1.

Tradeoffs: The scaffold records the requested model stack but does not call paid APIs until an explicit creator-approved submit path exists.

Follow-up: Confirm exact endpoint model identifiers from the Runway workflow registry after the custom workflow is created. Superseded for image generation by the Nano Banana pivot below after GPT Image 2 workflow nodes failed published API execution.

### 2026-05-09 — First Creator-Approved Runway Submit Path

Decision: Build the app integration around a published workflow named `TCS Seedance Director v1`, with a dry-run node-output preview and explicit creator approval before `POST /v1/workflows/{id}`.

Why: The project needs a demoable bridge from safe top-comment packages to Runway generation without accidentally spending credits or bypassing Bryan's review.

Alternatives considered: Calling Seedance directly from the app, waiting for the full workflow graph before adding app code, or auto-submitting as soon as a package is generated.

Tradeoffs: The local app can preview and submit once the workflow ID/node map exist, but final live generation remains blocked until the workflow is published and configured.

Follow-up: Create the Runway workflow, copy its published UUID, map all required input node IDs, and test the submit/status flow with a sample package.

### 2026-05-09 — Reference Clip Braid for Workflow V1.1

Decision: Keep the app-facing Runway workflow endpoint contract unchanged, but expand the internal Runway graph toward nine generated image references, three generated audio cues, three short Seedance reference clips, and one final Seedance hero clip.

Why: Three short reference clips can carry motion, pacing, texture, and payoff information into the final generation more richly than static first/last images alone.

Alternatives considered: Feed only two images into the final Seedance node, connect all generated images directly to the final node, or add new app-side inputs for every reference asset.

Tradeoffs: The graph becomes noisier and more credit-intensive, but the local API contract stays stable and the demo can fall back to sidecar reference clips if the final Workflows node does not expose video-reference ports.

Follow-up: Build a v1.1 workflow version with three reference clip nodes, verify final Seedance video-reference inputs in the Runway UI, publish a new endpoint UUID, and update local `.env` after the endpoint is stable.

### 2026-05-09 — GPT Image 2 Workflow Node Contract

Decision: Treat `gpt_image_2` as the canonical Runway API model slug for GPT Image 2 image generation and avoid workflow image nodes that publish as `appNodeType: gpt-tidepool-alpha`.

Why: Episode 3 workflow invocation surfaced `No model variant mapping for app node type: gpt-tidepool-alpha` on the Ref Image nodes, while the current Runway docs identify GPT Image 2 as `gpt_image_2` via the text/image-to-image API.

Alternatives considered: Keep the existing GPT image nodes and hide their outputs, or remove image references entirely from the workflow.

Tradeoffs: Rebuilding the image board costs workflow-editor time, but it preserves the richer multimodal design and avoids a brittle prompt-only fallback.

Follow-up: Rebuild the canvas image board with API-supported GPT Image 2 nodes, publish a new endpoint, inspect the graph, and only route images into Seedance after a small published endpoint proves the image node generates through the Workflow API.

### 2026-05-09 — Hackathon Image Lane Pivot To Nano Banana

Decision: Use Nano Banana Pro / Gemini 3 Pro Image (`gemini_image3_pro`) as the default image model for hackathon image references, with Nano Banana / Gemini 2.5 Flash (`gemini_2.5_flash`) as the fast fallback. Treat GPT Image 2 as unavailable for published Workflow API routing until Runway fixes the `gpt-tidepool-alpha` mapping path.

Why: Endpoint `ec5e1e70-0406-41e2-9195-08ef5e32f7c4`, invocation `23af7906-76c5-448f-8884-a6357025d924`, reproduced `No model variant mapping for app node type: gpt-tidepool-alpha` even after wiring a single GPT Image 2 node serially from the prompt workflow into final Seedance `firstFrame`. The Runway docs list `gemini_image3_pro` and `gemini_2.5_flash` as supported text/image-to-image API models.

Alternatives considered: Keep trying GPT Image 2 node variants, remove image references entirely, or rely only on sidecar Seedance clips.

Tradeoffs: Nano Banana requires a small docs/code pivot and may need a new Workflow node proof, but it keeps the richer multimodal design alive for the demo while avoiding a known broken model mapping.

Follow-up: Direct `POST /v1/text_to_image` proof succeeded as task `8f46769b-92d3-4412-8c96-89d5d4445f25` after switching the portrait ratio to `768:1344`. The app client now defaults Nano Banana Pro to high-resolution portrait `1536:2752` for direct Seedance first-frame handoff quality. `3072:5504` remains useful for max-quality previsuals, but the first raw PNG handoff attempt exceeded Seedance's 16 MB prompt-image asset limit.

### 2026-05-09 — Nano Banana Pro Direct API Proof

Decision: Use the direct Runway text/image-to-image API as the first proven Nano Banana path before adding or routing any Nano Banana Workflow nodes.

Why: `gemini_image3_pro` rejected the app's logical `1080:1920` Shorts ratio with a 400 validation response, but accepted the Runway-supported portrait ratio `768:1344`. Task `8f46769b-92d3-4412-8c96-89d5d4445f25` then completed `SUCCEEDED` with one image output. A later `3072:5504` proof also completed, but direct Seedance `promptImage` rejected that raw PNG as larger than 16 MB, so the handoff default is `1536:2752`.

Alternatives considered: Try another Workflow image node immediately, or keep using Seedance-only prompts with no static image references.

Tradeoffs: Direct image tasks sit outside the current Runway Workflow graph, but they prove the model and payload contract quickly and can supply first-frame/reference assets for the next Seedance checkpoint.

Follow-up: Direct first-frame handoff is proven. Nano Banana task `6abcc1e7-81ec-42fc-90e5-b0277e134d3f` at `1536:2752` fed Seedance image-to-video task `83e7205d-7e4f-4f8c-81ad-50b963fc0f66`, which completed `SUCCEEDED` with one video output. Next, rebuild the workflow image board around this direct handoff contract or add resizing/compression if max `3072:5504` images are required.

### 2026-05-10 — Dedicated Image Board Before Full Concert Workflow

Decision: Keep the stable hero MP4 endpoint on `e4a221ab-743d-45ac-bc47-633d66227614`, add a separate package-page nine-image board lane, and prove final Seedance MP4 generation with text-to-video image references before reintroducing video references.

Why: The three row image workflows already work independently, while earlier all-in-one `referenceVideos`/keyframe workflow checkpoints stalled or returned empty outputs. The Seedance docs distinguish image refs as `references` from video refs as `referenceVideos`, so the least risky next proof is nine images only.

Alternatives considered: Invoke another full workflow with image refs, video refs, and audio together; keep image generation script-only; or route the row images into final Seedance keyframes.

Tradeoffs: The app orchestration path is less visually elegant than a single Runway workflow graph, but it preserves demo reliability and keeps the working hero MP4 route unblocked.

Follow-up: App lane code and tests are in place. Direct Seedance task `5bf9b443-cdf0-443c-b752-9e292592e69b` was submitted with nine existing row images and completed `SUCCEEDED` with one MP4 output. Published all-in-one image-reference checkpoint `8ab20d96-444e-4751-aa91-9c0b44c5036c` was live-invoked as `f030c851-4eea-41ce-b3a3-7a5b3f86658d`; it crossed the earlier stall bands but finished `SUCCEEDED` with empty output and no failure metadata. Parser-normalized/no-audio endpoint `2866261a-9e0c-434e-8e32-b41da06ef9d4`, based on Runway's copied JSON example pattern, also finished empty on invocation `a2c33089-e7f0-48c5-bfaa-e531dff83833`. The demo path should stay on the app-side direct text-to-video `references` route.

### 2026-05-10 — Treat Workflow Seedance Image References As Blocked

Decision: Keep Seedance image references out of the hackathon Workflow endpoint path, and use the app-side direct Seedance `references` lane for image-referenced MP4 generation.

Why: Bryan's additional Runway examples prove Gemini-generated image chaining works inside Workflows, but they do not use Seedance. The closest example, `Storyboard to Film_example`, uses one generated Gemini image per Kling video node. TCS endpoint `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33` copied that one-image-per-video structure with Seedance instead of Kling, and invocation `53be6385-7dfb-4f89-b0e7-c7e61e393efc` still returned `SUCCEEDED` with empty output. Raw `curl.exe` Workflow invocation `a6eea7bd-f8b0-4fcb-bfca-68445d3f65b6` reproduced the same result, so SDK typed-field lag is not the cause for the Workflow endpoint. The final static asset diagnostic, endpoint `6ce25c70-8c4e-454b-9816-3c5569aff0f3`, removed generated Gemini image handoff entirely and routed a fixed Runway image asset into Seedance `referenceImages[0]`; invocation `f6f358be-d4b3-44dd-a407-2fd1b06b1228` also completed `SUCCEEDED` with empty output, no failure, and no node errors.

Alternatives considered: Keep iterating on nine-image Seedance `referenceImages`, add more concat/parser normalization, test a static uploaded asset, or switch the Workflow video nodes to Kling.

Tradeoffs: Staying with the direct Seedance lane is less elegant than a single Runway Workflow graph, but it preserves the proven demo path and avoids spending credits on a Seedance Workflow reference handoff that now fails in nine-image, one-image generated, and one-image static-asset forms. Switching to Kling may match the inspected example but would move away from the Seedance-centered project direction.

Follow-up: Keep Workflows responsible for the text-only hero route and image-board generation, with final image-referenced Seedance MP4s submitted directly from the app. Use `scripts/run_seedance_curl_diagnostic.ps1` when checking whether a future Seedance API behavior differs between curl and app code, and spend new exploration credits on direct Seedance, Gen 4.5, Veo 3.1, or upscaler adapter tests instead of more Seedance `referenceImages` Workflow shapes.

### 2026-05-10 — Replace TCS13 With Gen/Veo AV Director Packet

Decision: Stop treating the Seedance-shaped TCS13 field list as the active creative contract. Preserve Audience-in-the-Loop and creator approval, but generate a unified Gen/Veo audio-video director packet with audience signal, creator intent, subject continuity, scene world, visual anchor, motion arc, camera language, audio design, audio-video sync, and negative constraints.

Why: TCS13 was useful for maximizing Seedance 2.0 reference and prompt surface area. Gen-4.5 and Veo 3.1 have different public API constraints, especially one-image image-to-video input. A unified AV packet gives Veo the sound and image direction as one synchronized scene, while still letting Gen-4.5 use the visual/motion subset for silent cinematic studies.

Alternatives considered: Keep the TCS13 adapter unchanged, create separate audio and video prompts, or attempt to emulate Seedance internals directly.

Tradeoffs: This does not reproduce Seedance's private joint-generation architecture. It mimics the useful product-level behavior by planning audio and video together before the Runway call, then compressing that packet into the documented Gen/Veo prompt shape.

Follow-up: Re-map any published Runway workflow inputs to the new logical names (`av_director_packet`, `opening_frame_prompt`, `motion_prompt`, `audio_prompt`, and `sync_prompt`) before using the generic workflow submit button.

### 2026-05-10 — Model Adapter Methodology For Gen 4.5, Veo 3.1, And Upscaling

Status: Superseded for active app inputs by `2026-05-10 — Replace TCS13 With Gen/Veo AV Director Packet`. Historical rationale retained for the Seedance-to-Gen/Veo pivot.

Decision: Keep the 13 app inputs and Gemini/Nano Banana image-board methodology as the stable creative contract, then treat Seedance, Gen 4.5, and Veo 3.1 as interchangeable video adapters behind that contract. Treat upscaling as a post-generation package step after the video adapter returns a visible MP4.

Why: Seedance direct image references are proven and remain the demo baseline, but Gen 4.5 and Veo 3.1 may have different input capabilities. A model-adapter boundary lets TCS preserve audience creative fidelity from the same 13 inputs while testing which video model best honors the prompt, image board, motion plan, duration, and Shorts framing.

Alternatives considered: Rewrite the app around each model's native fields, keep Seedance only, or move upscaling into the first generation request.

Tradeoffs: The adapter approach adds a small planning layer, but it avoids hard-coding one model's reference semantics into the creator workflow and gives Bryan a clean comparison path across Seedance, Gen 4.5, and Veo 3.1.

Follow-up: Confirm exact Gen 4.5 and Veo 3.1 reference input shapes, duration/ratio limits, and whether a public Runway upscaler or Magnific API slug is available before wiring paid app calls. Keep the known-good Seedance/direct lane as the baseline until a candidate adapter produces and passes visual QA.

### 2026-05-10 — Gen/Veo Board, Sidecars, And Stitched Long Final

Decision: Preserve the proven 4-second Veo director lane, then add a separate asset-planner branch that produces a 9-panel Nano Banana Pro board, three Gen-4.5 image-to-video sidecar shots, and a 16-second stitched final made from four 4-second Veo 3.1 native-audio segments.

Why: The Workflow canvas has proven `seconds=4` for Veo 3.1 but rejected `seconds=10`, while the public video APIs document a 2-10 second range rather than 15-30 seconds. Stitching multiple proven 4-second Veo segments is the least risky in-graph path toward a 15-30 second final without relying on unsupported single-node duration settings.

Alternatives considered: Try a single 15-30 second Veo node, stitch outside Runway with app-side ffmpeg, or use only Gen-4.5 sidecars with no long final.

Tradeoffs: The all-in-one graph is expensive to run because it schedules 13 image generations, 7 video generations, and stitch operations. The visible 9-panel board also needs hidden duplicate start-frame image nodes for sidecars, because connected board outputs are not auto-exposed by the publish UI.

Follow-up: Use endpoint `c38549da-a2b8-4541-96a0-db14af640184` for static contract inspection only until Bryan explicitly approves a full paid invocation. If the stitched output behaves well, update the app `.env` and verifier around this Gen/Veo v2 contract.

### 2026-05-10 — One-Output Final Master Contract

Decision: Add a final master Stitch Videos node that combines the 4-second director preview branch with the 16-second asset-planner final, then expose only `final_final_video_20s` in the published Workflow endpoint.

Why: The prior graph was useful for visual debugging, but the product contract needs one final video output. The hidden board, sidecar, segment, and intermediate stitch nodes can still improve creative fidelity without cluttering the API response.

Alternatives considered: Keep exposing every board/sidecar output, run a second app-side finalization pass with ephemeral uploads, or stitch every sidecar plus the long final into a longer review reel.

Tradeoffs: Hiding outputs does not remove upstream generation cost; it only simplifies the app-facing contract. Ephemeral uploads remain useful for future second-stage API orchestration, but they are asset staging rather than the mechanism that combines videos inside the Workflow graph.

Follow-up: Use endpoint `26bf091b-6f75-49c4-bd74-4de137eef9ce` for static contract inspection. Run one paid smoke test only after Bryan approves the full upstream generation cost.

### 2026-05-10 — Adopt Storyboard-to-Short Continuity Spine

Decision: Adapt Runway's featured `Storyboard to Film` workflow pattern into a TCS `Storyboard-to-Short` graph before doing another major Gen/Veo final-output build.

Why: Paid smoke invocation `ce9d109c-8a3b-4fcf-9ae3-0ad1ecf6d16d` proved the final-master endpoint can produce a 20-second MP4 with AAC audio, but the contact sheet showed the stitched sections were not narratively continuous. The director preview and asset-planner final were generated from related but separate branches, so they did not share enough frame-to-frame visual memory.

Alternatives considered: Keep the branch-stitch master, expose intermediates for manual selection, or use ephemeral uploads as the main continuity mechanism.

Tradeoffs: Storyboard-to-short costs more graph design work and may require another checkpoint before paid testing, but it addresses the root cause: every final segment must derive from the same ordered storyboard, identity/world anchor, and prior-frame references. Ephemeral uploads help stage assets for second-stage calls; they do not make independently generated branches creatively coherent.

Follow-up: Build the next graph around one storyboard architect JSON output, sequential board/hero frame generation using previous-frame references, Veo 3.1 image-to-video segment generation from those frames, and Stitch Videos only at the end.

### 2026-05-09 — V1.1 Workflow Diagnostic Endpoint

Decision: Keep endpoint `8ae9c852-4319-417c-9d08-f389570b5db1` as a diagnostic V1.1 endpoint, but do not expand to the full nine-image/reference-clip braid until a smaller Seedance output path produces a final video URL.

Why: The endpoint accepts the app payload and exposes the final Seedance video, but invocation `8b5d57dd-7469-4b19-b572-3cc732237110` returned `SUCCEEDED` with an empty output object and `No model variant mapping for app node type: gpt-tidepool-alpha`. The GPT Image node now publishes with `taskType: workflow_gpt_image_2`, but still reports and executes as `appNodeType: gpt-tidepool-alpha`.

Alternatives considered: Continue adding all nine GPT Image nodes immediately, or revert to the older audio-producing endpoint.

Tradeoffs: Pausing expansion slows the creative graph build, but it avoids multiplying nodes before the final video path is proven.

Follow-up: Publish a tiny diagnostic endpoint with direct Combine Text to Seedance and no image edge. Keep GPT Image 2 out of the Workflow graph until Runway exposes an API-safe image node or move image generation to direct API calls.

### 2026-05-09 — Direct Seedance Diagnostic Endpoint

Decision: Publish endpoint `34abb3cb-1f88-4a2a-b5d4-3fc0888e9c36` with `TCS Input: script` wired directly into Seedance `textPrompt`, GPT Image hidden from outputs, and only Seedance `video` exposed.

Why: Manual canvas runs of Seedance fed by the JSON parser can produce video, but parsed text-only endpoint `4cec124c-3217-4435-844c-0b794dc2cdcc` still returned `SUCCEEDED` with an empty `output` object. A direct script-to-Seedance endpoint isolates whether the published Workflow API can return Seedance video at all.

Alternatives considered: Continue debugging parser outputs first, or rebuild the full reference-clip braid immediately.

Tradeoffs: This endpoint does not use the full director methodology, but it is the smallest useful API-facing proof for final video exposure.

Follow-up: Refresh invocation `e46ba302-ccde-4ff8-97fb-796b13e6de15`. If it returns video, reintroduce Claude/Parse; if it returns empty output, escalate the minimal direct Seedance endpoint as a Workflow API output issue.

### 2026-05-09 — True Minimal Seedance Workflow API Repro

Decision: Delete disconnected nodes from the diagnostic canvas and publish endpoint `5d1d6d5f-c194-4aaf-841a-bf68fa618425` with only two nodes: `TCS Input: script` and Seedance 2.0.

Why: Endpoint `45745fae-baed-498c-b84e-84c9ff5549bb` had only one edge, but Workflow API still executed disconnected model nodes and failed the disconnected Claude planner with an undefined prompt. A useful minimal repro must remove unused nodes, not just disconnect them.

Alternatives considered: Keep disconnected nodes for visual reference, or continue testing the app-facing 13-input contract.

Tradeoffs: The canvas no longer preserves the full V1.1 graph visually, but the published endpoint is clean enough to isolate Seedance output behavior.

Follow-up: Invocation `ba15f8c4-8363-4a6d-b16f-a117daf3b605` returned a Seedance MP4 URL with zero node errors. Rebuild the richer workflow incrementally from this two-node base and publish/test after each added node class.

### 2026-05-09 — 13-Input Checkpoint From Minimal Seedance Base

Decision: Publish endpoint `82d1f2da-0ed8-4bdc-8888-9c804852c2c1` after restoring the 13 app-facing text inputs around the proven two-node Seedance path, while keeping only `script -> Seedance.textPrompt` connected.

Why: The app needs its full logical payload contract, but the successful two-node test showed we should add only one category of complexity at a time. This checkpoint tests whether 13 exposed primitive inputs are safe when no extra model nodes exist.

Alternatives considered: Add Claude/Parse immediately, or keep using the one-input diagnostic endpoint.

Tradeoffs: The duplicated input nodes are API-valid but visibly mislabeled in the Runway UI, so this endpoint is a functional checkpoint rather than the polished workflow version.

Follow-up: Invocation `86d47202-4abe-4a40-8833-fd96947349c9` completed `SUCCEEDED` with one Seedance MP4 output and zero node errors. Clean up input labels/layout, then add a single planner/parser stage and publish/test again.

### 2026-05-09 — Polished 13-Input Layout Checkpoint

Decision: Publish endpoint `eee1e1d2-71e8-4cc5-a516-416ee71e1f89` after renaming the 13 input nodes and arranging them into non-overlapping canvas stages, while keeping the same `script -> Seedance.textPrompt` execution path.

Why: The previous 13-input checkpoint proved the API contract worked, but duplicated labels made the canvas and publish screen hard to reason about. The workflow needs clean visual telemetry before adding planner/parser nodes.

Alternatives considered: Add Claude/Parse immediately on top of the duplicate-label graph, or rebuild all inputs from scratch.

Tradeoffs: This checkpoint still does not add new model behavior, but it gives a clean, stable visual base for the next incremental stage.

Follow-up: Invocation `54d26e50-af62-4f2e-b936-a37a08a8a15c` completed `SUCCEEDED` with one Seedance MP4 output and zero node errors. Add one planner/parser stage in its own grouped column and publish/test before adding GPT Image or reference-clip braiding.

### 2026-05-09 — Planner/Parser Checkpoint Before Image References

Decision: Publish endpoint `07eab094-6c6a-46a4-9dfb-963d97a293f5` after adding exactly one Claude JSON planner, one Parse JSON node for `seedance_prompt`, and one hidden system prompt Text node between the existing `script` input and final Seedance node.

Why: The polished 13-input checkpoint works through the Workflow API, so the next safest increment is proving the text-planning path before adding GPT Image, audio, or reference-clip branches.

Alternatives considered: Add the full GPT text/image/reference-clip design immediately, or keep using the direct `script -> Seedance` prompt while moving planner logic app-side.

Tradeoffs: This endpoint still uses only `script` as the live prompt input to Claude, so the other 12 exposed app inputs are contract-preserving context for later wiring rather than active planner context. The graph stays easy to isolate and the node map remains unchanged.

Follow-up: Invocation `e1888b11-d1d5-4078-af20-c583746bad48` completed `SUCCEEDED` with one Seedance MP4 output. Add one GPT/text refinement layer next, preferably app-side/direct API unless a true GPT text node appears in the Runway picker, then publish/test before adding GPT Image or reference nodes.

### 2026-05-10 — Serial Combine Text and Claude Refiner Checkpoint

Decision: Keep text refinement inside Runway by using a second Claude text node, and feed all 13 app inputs into the planner through a serial Runway Combine Text chain instead of a parallel fan-in tree.

Why: The Runway picker did not expose a clean GPT text node, while Claude text boxes work natively in the workflow. Published parallel Combine endpoint `ff2496e8-f10b-4b2a-a98a-fa474bc0b599` returned `SUCCEEDED` with empty output and Combine node errors saying `Node is already running in this execution`; the serial chain avoids scheduling several Combine nodes against the same execution branch at once.

Alternatives considered: Keep the previous script-only planner input, move text refinement app-side, or keep the wide Combine tree and retry.

Tradeoffs: The serial chain is visually taller and adds latency, but it preserves the explicit 13-input app contract, keeps prompt shaping internal to Runway, and produced a successful published endpoint.

Follow-up: Endpoint `e4a221ab-743d-45ac-bc47-633d66227614` completed as invocation `de9c70e6-972a-44ca-ae16-119d3d1ab762` with one Seedance MP4 output and no node errors. Use this as the current text-only rich checkpoint before adding GPT Image or reference-clip branches.

### 2026-05-10 — Sidecar Seedance Reference-Clip Proof

Decision: Add one extra Seedance 2.0 node as a sidecar reference-clip proof before routing any reference video back into the final hero Seedance node.

Why: The final Seedance node exposes optional `referenceVideos`, but the safest next step is proving that a second Seedance node can run in the same published Workflow API invocation and expose its own video output without breaking the proven final branch.

Alternatives considered: Route the sidecar clip into final Seedance immediately, add all three reference clips at once, or test GPT Image first.

Tradeoffs: This proof costs one additional Seedance render and does not yet improve the final hero clip, but it establishes that Runway Workflows can return a sidecar motion-reference video in the same invocation.

Follow-up: Endpoint `b9beb013-0fe5-4f20-b244-a39b788ae95d` completed as invocation `06ee71a5-3e6e-4b36-ade3-7d199bada83a` with two Seedance MP4 outputs and no node errors. Later endpoint `1827e99b-ea37-44f2-8525-45c5e299369d` showed the risk: final Seedance stalled at 87.5% when all three reference clips were wired into `referenceVideos` alongside first/last keyframes.

### 2026-05-10 — Keep Reference Clips As Sidecar Outputs

Decision: Keep the three generated Seedance reference clips exposed as sidecar outputs and disable final Seedance `referenceVideos` in the current hackathon endpoint.

Why: The Seedance docs describe video references for text-to-video, but our final workflow node also uses first/last keyframes. Endpoint `1827e99b-ea37-44f2-8525-45c5e299369d` moved quickly through the three plain text-to-video reference clips, then stalled at 87.5% with no failure after the final node mixed `referenceVideos` with keyframes.

Alternatives considered: Retry the same endpoint, reduce to one `referenceVideos` edge, or remove keyframes from the final node.

Tradeoffs: The final hero clip no longer directly consumes reference videos, but the workflow still produces the reference clips as inspectable sidecar assets and avoids the observed stall path.

Follow-up: Endpoint `afd546a3-dbdb-4372-8aff-3a9c0e5282e8` disables final `referenceVideos` and keeps sidecar reference clips exposed, but it was later superseded by the keyframe-only endpoint after stalling at 72.5%.

### 2026-05-10 — Use Keyframe-Only Endpoint For Demo Reliability

Decision: Make the current local app endpoint a keyframe-only fast path: generate only the first and last Nano Banana reference images, feed those into final Seedance `firstFrame` and `lastFrame`, disable sidecar reference clips, and keep final Seedance `generateAudio` enabled.

Why: Endpoint `afd546a3-dbdb-4372-8aff-3a9c0e5282e8` stalled at 72.5%. Its graph has 40 runnable nodes, so 72.5% maps to 29/40 and likely sits inside the nine-image Nano Banana reference board before sidecar or final Seedance outputs complete. The hackathon demo needs one reliable final MP4 more than it needs the full reference board.

Alternatives considered: Wait longer on the nine-image board, reduce only the sidecar clips, or keep all nine images and hide outputs.

Tradeoffs: The workflow loses the richer nine-frame reference board for now, but the final hero path is shorter, cheaper, and easier to diagnose.

Follow-up: Endpoint `8923373c-fee1-4506-94b5-b9b8bd13370a` verifies with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-keyframe-only` and is the current local app endpoint.

### 2026-05-10 — Fall Back To Prompt-Only Workflow Endpoint

Decision: Make the current local app endpoint a prompt-only final Seedance workflow: keep the serial Combine/Claude planner/refiner path, feed final Seedance only through `textPrompt`, disable image refs and sidecar reference clips, and keep final Seedance `generateAudio` enabled.

Why: The keyframe-only endpoint crossed the previous 72.5% wall but invocation `f2071527-86b9-4471-81e3-ee769f20f051` finished `SUCCEEDED` with no exposed outputs. The previously proven serial Combine/refiner/final Seedance shape returned MP4s through the Workflow API, so the demo needs to return to that stable path.

Alternatives considered: Retry keyframe-only, keep only one keyframe image, or route through the direct Nano Banana -> Seedance lane.

Tradeoffs: The workflow output is less visually constrained than the image-ref versions, but it is the shortest reliable Runway Workflow path and still preserves Audience-in-the-Loop prompt direction.

Follow-up: Endpoint `9c0f1f38-e664-4b9e-9402-f2dae15b692b` verifies with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults`; graph inspection confirms final Seedance receives only `textPrompt` and exposes `video`.

### 2026-05-10 — Restore Known-Good Workflow Endpoint

Decision: Use endpoint `e4a221ab-743d-45ac-bc47-633d66227614` as the current local Workflow API endpoint for the demo fallback.

Why: Newly published endpoint `9c0f1f38-e664-4b9e-9402-f2dae15b692b` matched the old successful graph shape but still returned `SUCCEEDED` with no exposed outputs. Endpoint `e4a221ab-743d-45ac-bc47-633d66227614` has an actual historical app invocation, `de9c70e6-972a-44ca-ae16-119d3d1ab762`, that completed with one final Seedance MP4.

Alternatives considered: Keep retrying newly published endpoints, use corrected-default sidecar proof `691b3f2b-720c-4b45-ade1-3190a45b11d5`, or use the direct Nano Banana -> Seedance lane only.

Tradeoffs: The endpoint has duplicated Runway canvas defaults, so manual Runway runs are misleading. The local app route overrides every input and is the intended demo path.

Follow-up: `uv run python scripts/verify_runway_workflow_contract.py` passes against `e4a221...` with expected default warnings; strict mode should be reserved for corrected-default endpoints. Fresh app invocation `414d3a5a-8554-4b8b-ae31-2b2853c6f920` confirmed the endpoint still returns one MP4.

### 2026-05-10 — Split Hero Video And Image Board Workflows

Decision: Keep the hero MP4 workflow and image-board workflow as separate lanes.

Why: The known-good hero endpoint reliably returns a final MP4, while richer board endpoints have stalled or returned empty outputs. The demo should not make final video delivery depend on nine image generations, sidecar clips, or reference-video routing.

Alternatives considered: Attach the nine-image board back to final Seedance, use the keyframe-only endpoint as the hero path, or make the direct Nano Banana lane the only reference path.

Tradeoffs: The image board becomes an auxiliary asset package instead of part of the final hero invocation, but it can be tested and scaled independently without breaking the creator-approved MP4 route.

Follow-up: Complete. Row endpoints `f4ed6cf3-69b0-436b-a37c-82e1a7eeeb46`, `06a818f1-6dec-4cae-878d-ceeb6fbd5c2d`, and `fd051825-a295-4406-a80b-1fbfd8f8b7da` all completed `SUCCEEDED` with 3 image outputs each. Keep using the separated row workflows until the app has a dedicated image-board lane or a single nine-image-only endpoint is proven.

### 2026-05-10 — Pivot Hackathon Video Adapter To Gen-4.5 And Veo 3.1

Decision: Remove Seedance from the current hackathon app workflow. Keep Nano Banana Pro as the image-board source, use Gen-4.5 for silent cinematic shot studies, and use Veo 3.1 for final video because the final output needs native sound.

Why: Published Workflow diagnostics showed Seedance `referenceImages` returning `SUCCEEDED` with empty outputs across nine-image, one generated image, curl-invoked, and static-asset cases. The Runway public docs confirm Gen-4.5 and Veo 3.1 support direct text-to-video and image-to-video, while Veo is the appropriate final adapter for sound.

Alternatives considered: Continue with direct Seedance image references, try more published Seedance reference graph shapes, or add an unconfirmed upscaler/model slug.

Tradeoffs: Gen-4.5/Veo public image-to-video accepts only one prompt image, so the app uses the first board image as the visual anchor and compresses the remaining nine-image board plan plus the Gen/Veo AV director packet into the prompt. This is less literal than passing nine references, but it is aligned with the documented public API.

Follow-up: Confirm whether Runway exposes a public Precision v2/Magnific upscaler endpoint before automating image upscaling. Until then, keep upscaling manual/pending and do not block the demo on it.

### 2026-05-10 — Gen/Veo Workflow Director Stage

Decision: Add a serial Combine Text chain plus one Claude director node before the final Veo 3.1 node in the active Gen/Veo workflow.

Why: The one-edge checkpoint proved `av_director_packet -> Veo`, but the other nine app inputs were only exposed, not shaping the final prompt. Runway featured templates consistently use a planner/director stage before generation, and a serial chain avoids the scheduler issue seen with wide Combine fan-in.

Alternatives considered: Keep only `av_director_packet -> Veo`, add full JSON parser fanout and image board immediately, or use one wide Combine node.

Tradeoffs: This adds one Claude call and more graph nodes, but keeps the next checkpoint small, readable, and verified before expanding into Nano Banana boards or Gen-4.5 sidecars.

Follow-up: Update the workflow verifier for the Gen/Veo 10-input director graph before making endpoint `9ed1d223-c002-4f4d-b750-c43f0f3de8d8` the app's generic workflow endpoint.
