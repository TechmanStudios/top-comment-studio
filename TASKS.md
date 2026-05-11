# Hackathon Tasks

Use this as the shared task board for humans and AI agents.

## Status Legend

- `todo`
- `doing`
- `blocked`
- `done`

## Setup

| Status | Task | Notes |
|---|---|---|
| done | Identify stack and package manager | Recommended next-phase stack: Python/FastAPI/uv; implementation not added yet |
| done | Verify local install command | `uv sync` |
| done | Verify dev command | `uv run uvicorn top_comment_studio.app:app --reload` |
| done | Verify build command | No separate build command needed yet |
| done | Verify test command | `uv run pytest` |
| done | Create or update `.env.example` | Runway placeholders added; no real secrets |
| done | Run `scripts/agent_repo_audit.py` | Generated local `AI_REPO_AUDIT.md`, ignored by git |
| done | Create public GitHub repo | Created `https://github.com/TechmanStudios/top-comment-studio` as a public repository; local `origin` is configured |
| done | Ignore local browser session exports | Cookie/session/auth-state patterns added to `.gitignore` |
| done | Recommend MVP stack | Python/FastAPI/uv documented for the first implementation phase |

## MVP

| Status | Task | Notes |
|---|---|---|
| todo | Define MVP user flow | Keep demo-focused |
| done | Add Python/FastAPI scaffold | FastAPI app, templates, storage, sample data, and smoke tests added |
| done | Implement smallest end-to-end path | Local package generation, creator-approved Runway submit shell, and published workflow config path are implemented |
| done | Design Runway workflow chain | `TCS Seedance Director v1` contract documented and published in Runway |
| done | Add smoke test or validation check | `uv run pytest` covers package generation and mocked Runway workflow payload submission |
| doing | Add error states | Missing approval/config/secret and Runway API errors are surfaced on the package page |
| done | Publish first Runway workflow | Published output-fixed 1080p endpoint UUID `961b51c3-6d75-408f-b98c-464728c829b4` |
| done | Capture workflow node map | Node map captured in `docs/RUNWAY_WORKFLOW_BUILD_GUIDE.md`; add values to local `.env` |
| done | Document workflow build recipe | See `docs/RUNWAY_WORKFLOW_BUILD_GUIDE.md` |
| done | Pivot hackathon video adapter | App final-video path now uses Nano Banana board -> Veo 3.1; direct shot lane uses Nano Banana -> Gen-4.5. Seedance is retained only in historical diagnostics/docs. |
| doing | Build v1.1 reference-clip workflow | Director prompt updated to the final-output methodology. Published checkpoints now prove minimal Seedance, 13-input layout, planner/parser, serial Combine/refiner, one sidecar Seedance reference clip, corrected input defaults, the indexed nine-image board, parser output-name fix, a sidecar-free board, the safer sidecar-only reference-clip board, a keyframe-only fast path, and a text-only fallback. Endpoint `e4a221ab-743d-45ac-bc47-633d66227614` is the current local app checkpoint because historical app invocation `de9c70e6-972a-44ca-ae16-119d3d1ab762` and fresh app invocation `414d3a5a-8554-4b8b-ae31-2b2853c6f920` both completed `SUCCEEDED` with one final Seedance MP4. It has the proven serial Combine/Claude/refiner path feeding final Seedance `textPrompt`; image refs, sidecar clips, sidecar audio, final `referenceImages`, and final `referenceVideos` are disabled while final Seedance `generateAudio` remains enabled. Its canvas defaults are duplicated, but app submissions override all 13 inputs. Image-board work is now split into a separate lane and proven as three row workflows: row endpoint `f4ed6cf3-69b0-436b-a37c-82e1a7eeeb46` generated `Ref Image 01-03` via invocation `d99becc7-1da3-489a-a94e-c1bd4c693621`; row endpoint `06a818f1-6dec-4cae-878d-ceeb6fbd5c2d` generated `Ref Image 04-06` via invocation `f7360924-0e1f-479d-a223-0d53ff901813`; row endpoint `fd051825-a295-4406-a80b-1fbfd8f8b7da` generated `Ref Image 07-09` via invocation `dcfe5d44-e8f7-4bbf-9fdc-0da897b5f0ae`. Each completed `SUCCEEDED` with 3 image outputs, for 9 image outputs total. Use `uv run python scripts/run_runway_image_board_rows.py --status ...` to check row invocations without printing URLs. Newly published prompt-only endpoint `9c0f1f38-e664-4b9e-9402-f2dae15b692b` matched the graph shape but returned `SUCCEEDED` with no exposed outputs on invocation `4732c4b5-f714-48bf-8b8c-a5d0ac5f96d9`. Endpoint `8923373c-fee1-4506-94b5-b9b8bd13370a` crossed the old 72.5% wall but returned `SUCCEEDED` with no exposed outputs on invocation `f2071527-86b9-4471-81e3-ee769f20f051`. Endpoint `afd546a3-dbdb-4372-8aff-3a9c0e5282e8` stalled at 72.5% on invocation `97703298-5d9b-4048-9ef4-b47050fed0a5`, likely inside the nine-image Nano Banana board. Endpoint `1827e99b-ea37-44f2-8525-45c5e299369d` stalled at 87.5% on invocation `bfad2308-18e1-44d9-910e-f5ebafa8a39e`, likely when mixing final `referenceVideos` with first/last keyframes. Combined GPT Image 2 serial test endpoint `ec5e1e70-0406-41e2-9195-08ef5e32f7c4` reproduced `gpt-tidepool-alpha` model mapping failure. Direct Nano Banana Pro works at `768:1344` and high-res `1536:2752`; direct Seedance first-frame handoff is proven by Nano Banana task `6abcc1e7-81ec-42fc-90e5-b0277e134d3f` feeding Seedance task `83e7205d-7e4f-4f8c-81ad-50b963fc0f66`. |

## Demo Polish

| Status | Task | Notes |
|---|---|---|
| todo | Write demo script | See `docs/DEMO_SCRIPT.md` |
| todo | Add sample data | No secrets or private data |
| todo | Check fresh clone setup | Run from clean environment |
| todo | Document known limitations | See `KNOWN_ISSUES.md` |

## Agent Handoff Notes

Add dated notes here after major sessions.

```text
YYYY-MM-DD — Agent:
- Summary:
- Validation:
- Blockers:
- Next step:
```

```text
2026-05-11 — GitHub Copilot:
- Summary: Added a live deployment path for the judge URL. GitHub Pages is documented as static-only, while the working app should deploy to a server-backed Python/Docker host with Runway secrets stored in host environment variables. Added a root `Dockerfile`, `.dockerignore`, `render.yaml`, and `docs/LIVE_DEPLOYMENT.md` with Render Blueprint and Techman Studios subdomain/DreamHost DNS guidance.
- Validation: `uv run pytest` passed with 33 tests. `docker build -t top-comment-studio:deploy-check .` passed after Docker Desktop was started, and the container served `/health` on local port 8088.
- Blockers: Need the deployment files committed/pushed to GitHub before Render can import the Blueprint. Render account setup may require Bryan's browser login and payment/workspace selection.
- Next step: Commit/push the deployment files, open `https://render.com/deploy?repo=https://github.com/TechmanStudios/top-comment-studio`, enter the Runway secret when prompted, deploy, then point `top-comment.techmanstudios.com` or another subdomain at the Render service.
```

```text
2026-05-11 — GitHub Copilot:
- Summary: Simplified the Signal Intake demo path. The selected audience comment now has a real editable default value, so the form can render end-to-end without a browser required-field popup. The remaining optional prompt controls are still available, but collapsed under `Director controls` to keep the judge-facing path simple.
- Validation: `uv run pytest` passed with 33 tests. Browser check confirmed the homepage has the editable default signal, closed `Director controls`, no visible duration field, and `Generate render`.
- Blockers: None.
- Next step: During the demo, leave the default signal for the fastest run or replace only that one field to show audience-driven variation.
```

```text
2026-05-11 — GitHub Copilot:
- Summary: Ran one paid live v66 generation through the local app after restarting the stale FastAPI server on port 8001. The successful run is `episode_010` with Runway invocation `a31a299d-ffdc-47f4-ae24-600856271589`.
- Validation: The package page progressed from `Rendering` to `Render ready`; the saved record reports `status=SUCCEEDED`, one output URL, and no failure.
- Blockers: None for this run.
- Next step: Use the visible `Open video` action on the active package page to review the MP4 output.
```

```text
2026-05-11 — GitHub Copilot:
- Summary: Removed the user-editable duration field from Signal Intake and hard-coded the app's v66 workflow input to `duration_seconds=4`, matching the paid-proven four-second segment setting. Also hid the homepage render-output panel when the latest record has no active, blocked, or completed render, so the front page stays empty until `Generate render` actually starts a render state. Generate render now always attempts v66 submission and persists either an invocation or a visible blocked/error state.
- Validation: `uv run pytest` passed with 32 tests. Browser check confirmed the homepage has no `Duration seconds`, no idle `Render output` panel, and still shows `Generate render`. Local preview check confirmed v66 payload duration is `4`.
- Blockers: No paid live generation was run in this pass.
- Next step: Run one live Generate render when ready and confirm the package page immediately shows `Rendering` plus auto-refresh, then `Open video` when complete.
```

```text
2026-05-11 — GitHub Copilot:
- Summary: Removed the double-approval UX from the judge flow. The intake form now has one visible `Generate render` action that posts creator approval as a hidden value and starts the configured v66 workflow in the same request. The package/render page no longer shows a creator-approval checkbox or `Start render`; it only shows status/progress, refresh while active, and video/open actions when complete.
- Validation: `uv run pytest` passed with 31 tests, including route coverage proving `/package` starts the workflow without a second approval click and package-page coverage proving the old start controls are absent. Browser check confirmed the home page shows `Generate render`, no visible approval checkbox, and no `Generate package` copy.
- Blockers: No paid live generation was run in this pass.
- Next step: Rehearse with a live safe prompt once, then let the package page sit as the render monitor until the MP4 appears.
```

```text
2026-05-11 — GitHub Copilot:
- Summary: Replaced the dense package dashboard with a single judge-facing render page. The page now shows only render status, progress, start/refresh controls, and an embedded video player plus `Open video` action when output exists. Internal package details, workflow debug output, image board rows, and direct-generation panels are no longer rendered on the main package page.
- Validation: `uv run pytest` passed with 30 tests, including a regression test that rejects the old dense package sections. Browser check at `/package/episode_003` confirmed the simplified render page is live and the old sections are absent. `git diff --check` reported only existing CRLF normalization warnings.
- Blockers: No paid live generation was run in this pass.
- Next step: Use the package page as the judge-facing output screen; keep internal diagnostics in code/routes only unless a separate admin/debug view is needed later.
```

```text
2026-05-11 — GitHub Copilot:
- Summary: Matched the Signal Intake and homepage render panels to the Techman Studios AI Labs card language with a dark shell, thin border, and warm-to-cyan top rail. Removed the old Latest Chain Checkpoint box and replaced it with a simple render output panel that shows v66 workflow status, progress, and either refresh or view-rendered-content action.
- Validation: `uv run pytest` passed with 29 tests. FastAPI homepage render smoke returned 200 and confirmed the old latest-chain copy is gone. Browser check at `http://127.0.0.1:8001/` confirmed the updated frame treatment and render panel are served.
- Blockers: None.
- Next step: Reuse the render panel space for any judge-facing output controls, keeping the page centered on one clear package-to-render flow.
```

```text
2026-05-11 — GitHub Copilot:
- Summary: Wired the intake `Generate package` flow to optionally start the configured v66 Runway workflow when `Creator-approved for v66 Runway generation` is checked. Centralized rendered-video URL selection so the v66 workflow output takes priority over older board/direct fallback outputs, updated package-page auto-refresh to poll the correct status endpoint, and refreshed `.env.example` with the v66 endpoint/node map.
- Validation: `uv run pytest` passed with 29 tests. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains --require-seamless-transition-keyframes --require-1080p-video` passed against endpoint `c1b49d17-c80f-4705-b0e6-86c89a070464`. FastAPI TestClient render smoke returned 200 for `/` and `/package/episode_003`.
- Blockers: No paid live generation was run in this pass.
- Next step: In the browser, check the v66 approval box on a safe comment and generate one package during rehearsal to confirm the returned MP4 replaces the latest `Open rendered video` link.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Expanded `docs/RUNWAY_WORKFLOW_AGENT_HELP.md` and `docs/RUNWAY_WORKFLOW_BUILD_GUIDE.md` with a reusable programmatic Runway workflow engineering playbook. The new notes cover the canvas/editor API vs Developer API split, safe save/publish/verify order, graph mutation rules, stable TCS node naming, parser fanout and concat normalization, scalar Veo `startFrame`/`endFrame` routing, app node type mappings, 720p vs 1080p lessons, featured workflow harvesting, and the validation ladder from internal graph validation to paid smoke and local artifact inspection.
- Validation: VS Code reported no Markdown problems for the edited docs. Direct trailing-whitespace scans found no matches in the Runway docs or `TASKS.md`. `git diff --check -- docs/RUNWAY_WORKFLOW_AGENT_HELP.md docs/RUNWAY_WORKFLOW_BUILD_GUIDE.md TASKS.md` passed for tracked changes with only the existing CRLF normalization warning for `TASKS.md`.
- Blockers: None.
- Next step: Use these docs as the starting point before designing the next app engineering and workflow variants.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Published corrected version 66 endpoint `c1b49d17-c80f-4705-b0e6-86c89a070464` as the current 1080p seamless-keyframe Continuity Core checkpoint. It keeps the version 63 seamless transition design, sets all four Veo 3.1 segment nodes to `resolution=1080p`, spaces the generated-frame/enhancer/video rows for easier visual inspection in the Runway editor, restores the TCS input output labels, and exposes `final_storyboard_short_16s` from the final Stitch Videos node. Local `.env` now points to this endpoint. Do not use intermediate endpoint `c5882933-e837-432d-b59e-d255be020d29`; that version 65 publish dropped input labels and the exposed final output.
- Validation: Internal Runway `/v1/dynamic_workflows/validate` passed before saving/publishing version 66. Published Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains --require-seamless-transition-keyframes --require-1080p-video`. Paid smoke invocation `f805c55d-4ed3-461a-ac82-1153c828904b` completed `SUCCEEDED` with one MP4 and empty node errors. `ffprobe` found AAC audio duration about 16.085 seconds and H.264 video duration about 16.042 seconds at 1080x1920. Artifact: `data/local/runway_outputs/f805c55d-4ed3-461a-ac82-1153c828904b_6e092b87-1cef-4b69-8a78-3a62fb08869f_item_1.mp4`; contact sheet: `data/local/runway_outputs/f805c55d-4ed3-461a-ac82-1153c828904b_contact_sheet.jpg`; safe result note: `data/local/runway_outputs/f805c55d-4ed3-461a-ac82-1153c828904b_result.json`.
- Blockers: No current blocker. Version 66 is the 1080p demo checkpoint; version 63 remains the 720p seamless-keyframe fallback if 1080p latency or credit cost becomes an issue.
- Next step: Visually inspect the refreshed Runway editor layout and the local v66 MP4, then make only layout/prompt tweaks unless the 1080p runtime output reveals a real artifact.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Published version 63 endpoint `65e09485-4169-41d9-9282-85b52148949f` as the seamless-keyframe Continuity Core checkpoint. It keeps the version 62 Photo Enhancer chains, adds Story Panels-inspired continuity guidance from featured workflow `529`, and borrows the Seamless Transitions pattern from featured workflow `364` by routing enhanced frames 02/03/04 into the previous Veo segment's scalar `endFrame`. The first three Veo 3.1 segments now use `workflow-veo3-1-keyframes-task`; the final payoff segment keeps the proven standard task. Local `.env` now points to this endpoint as the current demo workflow.
- Validation: Internal Runway `/v1/dynamic_workflows/validate` passed before saving/publishing version 63. Published Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains --require-seamless-transition-keyframes`. The new verifier flag also leaves version 62's original verification path passing. Paid smoke invocation `f6522ddd-ec5c-486f-80a3-a50906993ea8` completed `SUCCEEDED` with one MP4 and empty node errors. `ffprobe` found AAC audio duration about 16.085 seconds and H.264 video duration about 16.042 seconds at 720x1280. Artifact: `data/local/runway_outputs/f6522ddd-ec5c-486f-80a3-a50906993ea8_6e092b87-1cef-4b69-8a78-3a62fb08869f_item_1.mp4`; contact sheet: `data/local/runway_outputs/f6522ddd-ec5c-486f-80a3-a50906993ea8_contact_sheet.jpg`; safe result note: `data/local/runway_outputs/f6522ddd-ec5c-486f-80a3-a50906993ea8_result.json`. `uv run pytest` passed with 27 tests.
- Blockers: No current blocker. Version 63 keeps the same generation-cost profile as version 62, but adds Veo `endFrame` keyframe routing that should be watched during rehearsals.
- Next step: Use version 63 as the current seamless-keyframe demo checkpoint; keep version 62 as the paid-proven fallback if a future run shows keyframe transition artifacts.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Wired the Runway featured workflow `596` Photo Enhancer method into the current Continuity Core canvas. Version 61 endpoint `6e9bac23-016f-4f40-857e-d846132623ac` published/static-verified but failed paid smoke because the copied Gemini API nodes used runtime-invalid `appNodeType: gemini-api`. Published version 62 endpoint `277aecec-43a4-4042-844e-e9e3d41db8d3`, which fixes those nodes to `appNodeType: gemini` and keeps the enhancer chains between each Gemini storyboard frame and the corresponding Veo 3.1 `startFrame`.
- Validation: Runway internal `/v1/dynamic_workflows/validate` passed before saving/publishing version 62. Published Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core --require-photo-enhancer-chains` against endpoint `277aecec-43a4-4042-844e-e9e3d41db8d3`. Paid smoke invocation `cc30e6ea-f938-45b7-8d56-8ac62c314c67` completed `SUCCEEDED` with one MP4 and no node errors. `ffprobe` found AAC audio duration about 16.085 seconds and H.264 video duration about 16.042 seconds at 720x1280. Artifact: `data/local/runway_outputs/cc30e6ea-f938-45b7-8d56-8ac62c314c67_6e092b87-1cef-4b69-8a78-3a62fb08869f_item_1.mp4`; contact sheet: `data/local/runway_outputs/cc30e6ea-f938-45b7-8d56-8ac62c314c67_contact_sheet.jpg`; safe result note: `data/local/runway_outputs/cc30e6ea-f938-45b7-8d56-8ac62c314c67_result.json`.
- Blockers: No current blocker. Version 62 adds 16 Gemini API calls plus 8 extra Gemini Image Pro calls per full workflow invocation, so version 59 remains the cheaper fallback if needed.
- Next step: Use version 62 as the current photo-enhanced demo checkpoint; keep an eye on credit cost during rehearsals.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Wired the previously dangling `TCS Asset Parser: boards sidecars segments` into the Continuity Core creative process. Added `TCS Asset Planner: parsed creative map`, connected all 17 parsed outputs from board prompts, sidecar prompts, segment prompts, and continuity notes into that map, then fed the map into `TCS Continuity Core: enriched creative brief` as input index 2. Saved canvas version 59 and published endpoint `31f64606-73bf-4b43-ba53-596e92fc26bd`. Added `scripts/run_runway_workflow_smoke.py` and ran the approved paid smoke.
- Validation: Runway internal `/v1/dynamic_workflows/validate` passed before saving/publishing version 59 with 41 nodes and 72 edges. Published Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core`, and the verifier now requires the parser -> parsed creative map -> Continuity Core path. Paid smoke invocation `cc086bdd-3a14-4290-a6e8-bbb7c7f10788` completed `SUCCEEDED` with one MP4 and no node errors. `ffprobe` found AAC audio duration about 16.085 seconds and H.264 video duration about 16.042 seconds at 720x1280. Artifact: `data/local/runway_outputs/cc086bdd-3a14-4290-a6e8-bbb7c7f10788_6e092b87-1cef-4b69-8a78-3a62fb08869f_item_1.mp4`; contact sheet: `data/local/runway_outputs/cc086bdd-3a14-4290-a6e8-bbb7c7f10788_contact_sheet.jpg`; safe result note: `data/local/runway_outputs/cc086bdd-3a14-4290-a6e8-bbb7c7f10788_result.json`.
- Blockers: No blocker for version 59. Local `.env`/demo config has not been repointed to the new paid-proven endpoint yet.
- Next step: Point local `.env`/demo config at endpoint `31f64606-73bf-4b43-ba53-596e92fc26bd` when ready, then use version 59 as the current Continuity Core demo checkpoint.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Reorganized Runway canvas `ba325b07-a845-4fe6-901e-9242666ef8c7` visually after the successful Continuity Core smoke. Saved canvas version 58 as a layout-only update with all 40 nodes moved into clean lanes: TCS inputs, serial Combine chain, outer Director/Asset Planner ring, Continuity Core intake, storyboard director/parser/anchor, four frames, four Veo `startFrame` segments, stitches, and final output.
- Validation: Runway internal `/v1/dynamic_workflows/validate` passed before saving version 58 with 40 nodes and 55 edges. Readback from the browser confirmed version 58 positions, including `TCS Continuity Core: enriched creative brief` at `(5100, 620)`, storyboard anchor at `(6200, 80)`, frame 01 at `(6750, 0)`, segment 01 at `(7350, 0)`, and final stitch at `(8500, 600)`. Published endpoint `dbe78d91-05ca-460d-a71f-568164577793` still passed `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core`.
- Blockers: Version 58 was not published because it only changes visual positions; published version 57 remains the paid-proven app endpoint.
- Next step: Use the cleaned canvas layout for any future graph additions; publish only if functional graph inputs/outputs change or Runway requires a published visual snapshot.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Built and published the TCS Continuity Core checkpoint on canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`. New endpoint `dbe78d91-05ca-460d-a71f-568164577793`, version 57, preserves the paid-proven Storyboard-to-Short spine and adds the outer TCS Director and TCS Asset Planner groupings upstream of it. The new text-planning ring feeds `TCS Continuity Core: enriched creative brief`, which now drives `TCS Storyboard Director: continuity JSON` before the anchor, four frames, four Veo 3.1 `startFrame` segments, and final stitch.
- Validation: Runway internal `/v1/dynamic_workflows/validate` passed before save/publish with 40 nodes and 55 edges. Published Developer API verification passed with `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-continuity-core`. Paid smoke invocation `e0b2d638-7276-41d8-ad29-6d166e80fd96` completed `SUCCEEDED` with one MP4 and no node errors. `ffprobe` found AAC audio duration about 16.085 seconds and H.264 video duration about 16.042 seconds at 720x1280. Artifact: `data/local/runway_outputs/e0b2d638-7276-41d8-ad29-6d166e80fd96_final_storyboard_short_16s.mp4`; contact sheet: `data/local/runway_outputs/e0b2d638-7276-41d8-ad29-6d166e80fd96_contact_sheet.jpg`; raw result note: `data/local/runway_outputs/e0b2d638-7276-41d8-ad29-6d166e80fd96_result.json`.
- Blockers: No current runtime blocker. Creative note: contact sheet is the strongest continuity checkpoint so far; the floating city is the first-beat subject, remains recognizable through the storm lift, and resolves into a warm golden payoff.
- Next step: Point local `.env`/demo config at endpoint `dbe78d91-05ca-460d-a71f-568164577793` when ready to make Continuity Core the default app workflow.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Saved and published the TCS Storyboard-to-Short continuity graph on canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`. Version 55 endpoint `1766f759-d1ec-4cce-9a82-7386e8a72983` statically verified but failed the first paid smoke because the Veo segment nodes needed scalar `startFrame`, not indexed `promptImage[0]`. Fixed and republished version 56 endpoint `4af4b372-b117-49bd-9a7e-4812430f76eb` with four Veo 3.1 image-to-video segments fed by scalar `startFrame` edges.
- Validation: Published endpoint `4af4b372-b117-49bd-9a7e-4812430f76eb` passed `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-storyboard-to-short`. Paid smoke invocation `4b700e61-d835-433b-b330-5f58f2cefa8f` completed `SUCCEEDED` with one MP4 and no node errors. `ffprobe` found AAC audio duration about 16.085 seconds and H.264 video duration about 16.042 seconds. Artifact: `data/local/runway_outputs/4b700e61-d835-433b-b330-5f58f2cefa8f_final_storyboard_short_16s.mp4`; contact sheet: `data/local/runway_outputs/4b700e61-d835-433b-b330-5f58f2cefa8f_contact_sheet.jpg`.
- Blockers: No current runtime blocker. Creative note: the contact sheet is much more continuous than the branch-stitch endpoint, but the first beat features a small robot guide before the floating city becomes the main subject.
- Next step: Point local `.env`/demo config at endpoint `4af4b372-b117-49bd-9a7e-4812430f76eb` when ready to make Storyboard-to-Short the app default; avoid further paid graph changes unless refining the first-beat prompt to keep the city as the primary subject from frame one.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Continued the next-best-step continuity build. Replaced the legacy Seedance workflow verifier with a Gen/Veo-aware verifier that supports `--require-final-master` and `--require-storyboard-to-short`. Tested a no-credit in-memory Storyboard-to-Short mutation of canvas `ba325b07-a845-4fe6-901e-9242666ef8c7` through Runway's internal validator; it passed with 34 nodes, 47 edges, one anchor image, four sequential storyboard frames, four Veo 3.1 image-to-video segments, final stitch only, and one exposed generated output `final_storyboard_short_16s`.
- Validation: `uv run python -m py_compile scripts/verify_runway_workflow_contract.py` passed; `uv run pytest` passed 27 tests; Runway internal `/v1/dynamic_workflows/validate` returned `valid: true` for the Storyboard-to-Short graph mutation. No credits spent.
- Blockers: The mutation has not been saved or published to the Runway canvas yet. The true Veo 3.1 workflow image-input field still needs one published/static checkpoint and likely one tiny paid smoke to prove actual generation, because internal graph validation accepts several possible image-input names.
- Next step: Save the validated Storyboard-to-Short graph as a new canvas checkpoint, publish it, retrieve the published endpoint graph, update `RUNWAY_WORKFLOW_NODE_MAP_JSON`, run `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-storyboard-to-short`, then ask Bryan before any paid smoke.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Ran the approved paid smoke for final-master endpoint `26bf091b-6f75-49c4-bd74-4de137eef9ce`. Invocation `ce9d109c-8a3b-4fcf-9ae3-0ad1ecf6d16d` completed `SUCCEEDED` with one exposed MP4 and no node errors. Downloaded artifact: `data/local/runway_outputs/ce9d109c-8a3b-4fcf-9ae3-0ad1ecf6d16d_final_final_video_20s.mp4`; contact sheet: `data/local/runway_outputs/ce9d109c-8a3b-4fcf-9ae3-0ad1ecf6d16d_contact_sheet.jpg`.
- Validation: `ffprobe` confirmed AAC audio duration about 20.105 seconds and H.264 video duration about 20.042 seconds. The contact sheet showed a useful technical proof but weak creative continuity: the city changes form across stitched sections.
- Blockers: The current branch-stitch design is not the right final creative architecture, even though it works technically. Do not spend more on this exact shape except for regression checks.
- Next step: Adapt Runway featured workflow `661` (`Storyboard to Film`) into a TCS `Storyboard-to-Short` continuity spine: one storyboard architect JSON, one identity/world anchor, sequential frame generation with previous-frame references, Veo 3.1 image-to-video segments from those frames, then final Stitch Videos output.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Added the final-final Runway master output to canvas `ba325b07-a845-4fe6-901e-9242666ef8c7`. New endpoint `26bf091b-6f75-49c4-bd74-4de137eef9ce` keeps the 10-input Gen/Veo graph, hides the board/sidecar/intermediate outputs from the API contract, and exposes only `final_final_video_20s` from `TCS Final Final: director + asset master`. Also added REST client support for Runway ephemeral uploads so future app-side second-stage runs can convert local/downloaded assets into short-lived `runway://` URIs.
- Validation: Runway internal validation passed before save. Developer API retrieval confirmed version 54, 48 nodes, 54 edges, 10 exposed TCS inputs, one exposed generated output (`final_final_video_20s`), and no workflow nodes missing `appNodeType`. VS Code diagnostics found no errors in the edited client/test files. `uv run pytest` passed with 27 tests. `uv run python scripts/agent_repo_audit.py` completed. `git diff --check` reported only existing CRLF normalization warnings.
- Blockers: No paid invocation was run; hiding outputs does not reduce the upstream image/video generation cost. The app `.env` was not updated automatically.
- Next step: Update the Gen/Veo verifier for endpoint `26bf091b-6f75-49c4-bd74-4de137eef9ce`, then run one paid smoke test only after Bryan approves the full generation spend.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Expanded Runway canvas `ba325b07-a845-4fe6-901e-9242666ef8c7` into the Gen/Veo board/sidecar/long-final checkpoint. New endpoint `c38549da-a2b8-4541-96a0-db14af640184` preserves the 10-input director/Veo preview lane and adds hidden asset planning, JSON parser fanout, 9 terminal Nano Banana Pro board panels, 3 hidden sidecar-start images, 3 Gen-4.5 sidecar videos, 4 Veo 3.1 native-audio segments, and Stitch Videos nodes for `long_final_video_16s`.
- Validation: Runway internal validation passed with zero warnings before publish. Developer API retrieval confirmed version 52, 47 nodes, 52 edges, 10 exposed TCS inputs, 14 exposed outputs (`final_video_4s_preview`, `board_panel_01`-`board_panel_09`, `sidecar_shot_01`-`sidecar_shot_03`, `long_final_video_16s`), and no workflow nodes missing `appNodeType`.
- Blockers: No paid invocation was run; a full call would generate 13 images, 7 videos, and stitch outputs. The app `.env` was not updated automatically.
- Next step: Update the Gen/Veo verifier for this endpoint shape, then run a full paid invocation only after Bryan confirms the credit spend.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Reviewed Runway's Team Runway and Creative Partners featured workflow galleries, then upgraded canvas `ba325b07-a845-4fe6-901e-9242666ef8c7` from the one-edge Gen/Veo checkpoint into a true 10-input director-stage graph. New endpoint `9ed1d223-c002-4f4d-b750-c43f0f3de8d8` has 22 nodes, 21 edges, 10 exposed TCS inputs, 9 serial Combine Text nodes, one hidden Claude director system prompt, one Claude director node, and one Veo 3.1 final output labelled `final_video`.
- Validation: Runway internal graph validation passed before save. Developer API retrieval confirmed endpoint `9ed1d223-c002-4f4d-b750-c43f0f3de8d8` has 10 mapped inputs, 9 combine nodes, 1 Claude node, 1 Veo node, `seconds=4`, `aspectRatio=9:16`, `resolution=720p`, and `noAudio=false`. Paid test invocation `201a6753-3100-4b01-92fb-14698be41309` completed `SUCCEEDED` with no node errors and one MP4; `ffprobe` found H.264 video and AAC audio. Downloaded test artifact is local at `data/local/runway_outputs/201a6753-3100-4b01-92fb-14698be41309_final_video.mp4`.
- Blockers: Do not update `.env` automatically yet; local app config still points at the historical stable endpoint. Also note that old local episode JSON files may have blank AV packet fields, so regenerate packages or send complete logical inputs before using this endpoint from the app.
- Next step: Update the Gen/Veo workflow verifier and then decide whether `9ed1d223-c002-4f4d-b750-c43f0f3de8d8` should become the app's generic `RUNWAY_WORKFLOW_ID`.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Built and published the new grouped Runway Gen/Veo workflow canvas `ba325b07-a845-4fe6-901e-9242666ef8c7` as `TCS Gen/Veo AV Director v1`. The readable graph now has 10 TCS Text input nodes arranged by domain columns (metadata/control, audience/AV packet, visual-motion, audio-sync) feeding a final Veo 3.1 output lane. Published grouped endpoint `35a20104-42a9-4339-90b3-0b1e65259667` has 11 nodes, 10 exposed constant inputs, one AV-packet-to-Veo edge, `final_video` exposed, `aspectRatio=9:16`, `seconds=4`, and `noAudio=false`.
- Validation: Developer API retrieval confirmed endpoint `35a20104-42a9-4339-90b3-0b1e65259667` has 11 nodes, 10 constant inputs, and one Veo 3.1 node. Earlier tiny endpoint `eb2c561f-7a3f-4986-9847-213e36e14a60` invocation `a0c788cf-2f72-4c7a-a944-b2b23a6d6b69` completed `SUCCEEDED` with one MP4 output. Corrected grouped invocation `7709e9f9-6b9c-4dc0-8b37-5e541e2b0b43` completed `SUCCEEDED` with one exposed MP4 output and no node errors; `ffprobe` found one video stream and one AAC audio stream.
- Blockers: Endpoint `fb490b2c-aa0e-4e31-95eb-12b88c7bc6fc` used `seconds=10` and returned `SUCCEEDED` with empty output plus node error `Invalid task options: seconds: Invalid input`, so the Workflow checkpoint uses 4 seconds until another canvas-supported Veo duration is proven.
- Next step: Capture endpoint `35a20104-42a9-4339-90b3-0b1e65259667` and its node map in local `.env` only after deciding this Workflow path should become the app's generic submit endpoint.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Removed Seedance from the current hackathon app workflow. Direct generation now creates a Nano Banana first frame and advances it into Gen-4.5 image-to-video for a silent cinematic shot. The nine-image board final-video action now uses Veo 3.1 image-to-video with one hero board image as `promptImage`, while the prompt carries the ordered nine-image board plan for continuity and native audio direction.
- Validation: `uv run pytest` passed with 26 tests. `git diff --check` reported only existing CRLF normalization warnings.
- Blockers: Public docs did not reveal a Precision v2/Magnific upscaler API endpoint or model slug, so upscaling remains manual/pending rather than automated.
- Next step: Only make paid Gen-4.5/Veo calls after explicit creator approval; confirm a public Precision v2 upscaler endpoint before automating that stage.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Replaced the active Seedance-era TCS13 creative contract with a Gen/Veo unified AV director packet. The package form now accepts subject continuity, scene world, motion arc, camera language, audio design, and quality constraints; the generated package stores those as one synchronized audio-video brief for Gen-4.5 shot studies and Veo 3.1 native-audio final videos.
- Validation: `uv run pytest` passed with 26 tests after the source/test updates.
- Blockers: Existing published Runway workflow node maps must be remapped to the new logical input names before using the generic workflow submit path.
- Next step: Use the package page to inspect the AV packet before spending credits on a live Veo 3.1 final video.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Ran the remaining useful Seedance Workflow diagnostic by publishing endpoint `6ce25c70-8c4e-454b-9816-3c5569aff0f3`, which removes the generated Gemini image node and feeds a fixed Runway image asset into final Seedance `referenceImages[0]`. Also documented the model-adapter methodology for preserving the same 13 app inputs and Gemini/Nano Banana image-board method while testing Seedance, Gen 4.5, Veo 3.1, and post-generation upscaling.
- Validation: Curl invocation `f6f358be-d4b3-44dd-a407-2fd1b06b1228` reached 75% and completed `SUCCEEDED` with `output_count: 0`, no failure, and no node errors. Direct Seedance image references remain proven via task `5bf9b443-cdf0-443c-b752-9e292592e69b` and curl task `b988c359-4afe-4609-875c-e484b410e57d`, both of which returned output.
- Blockers: Seedance `referenceImages` inside published Workflows now fail empty in nine-image generated, one-image generated, curl-invoked one-image, and one-image static-asset forms.
- Next step: Stop spending credits on additional Seedance `referenceImages` Workflow shapes. Keep the demo on app-side direct Seedance `references`, and test Gen 4.5 / Veo 3.1 / upscaler adapters only after confirming exact supported payload fields and limits.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Inspected Bryan's additional Runway examples `60398763-9b47-473a-8ca3-066465d39bbc` (`Storyboard to Film_example`) and `e309a30a-364d-4bc0-ae4e-e43db1552c8a` (`JSON_StoryPanelsEX`). They confirm Gemini-generated images can chain through Workflows, but neither uses Seedance; Storyboard-to-Film routes one generated Gemini image into one Kling video node via `referenceImages[0]`. Published TCS endpoint `7ab7c6c7-6f54-4d40-a838-63fa72b1fe33` to test the closest Seedance equivalent: one generated Gemini image into final Seedance `referenceImages[0]`, 5-second duration, `generateAudio=false`, final video exposed.
- Validation: Invocation `53be6385-7dfb-4f89-b0e7-c7e61e393efc` completed `SUCCEEDED` with empty output and no failure metadata. Raw `curl.exe` Workflow invocation `a6eea7bd-f8b0-4fcb-bfca-68445d3f65b6` reproduced the same `SUCCEEDED` empty-output result, ruling out Python SDK/client typed-field drift for this Workflow endpoint. Direct curl Seedance task `b988c359-4afe-4609-875c-e484b410e57d` completed `SUCCEEDED` with one output. Added `scripts/run_seedance_curl_diagnostic.ps1` to submit/check direct Seedance and Workflow diagnostics through curl with sanitized output.
- Blockers: Generated Gemini image outputs feeding Seedance references inside Workflows appear blocked even in the one-image case.
- Next step: Do not spend more credits on generated-Gemini-to-Seedance-reference Workflow shapes. If more Workflow diagnosis is needed, test Seedance `referenceImages` from a static asset/input image; otherwise keep the demo on the proven app-side direct Seedance `references` lane.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Added the dedicated package-page nine-image reference-board lane. The app now persists row workflow state, submits/checks the three proven row endpoints, displays row progress/thumbnails, and can submit a final Seedance text-to-video task using the nine image URLs as `references`. Also published workflow checkpoint `8ab20d96-444e-4751-aa91-9c0b44c5036c`, which routes all nine generated images into final Seedance `referenceImages` and removes `firstFrame`, `lastFrame`, and `referenceVideos`.
- Validation: `uv run pytest` passed with 26 tests after the app changes. Direct Seedance task `5bf9b443-cdf0-443c-b752-9e292592e69b` was submitted with the existing nine row images and completed `SUCCEEDED` with one MP4 output. Local UI check at `http://127.0.0.1:8003/package/episode_001` found 3 row cards, 9 thumbnails, and 1 board MP4 output. Paid all-in-one workflow invocation `f030c851-4eea-41ce-b3a3-7a5b3f86658d` on endpoint `8ab20d96...` finished `SUCCEEDED` with empty output and no failure metadata.
- Additional diagnostic: Copied Runway `JSON_example` workflow `14139cd0-d760-4ee9-9a47-90f7324f06a9` showed that JSON parser fanout uses edge `from.index` plus concat normalizers. Endpoint `2866261a-9e0c-434e-8e32-b41da06ef9d4` applied that pattern to TCS and disabled final generated audio, but invocation `a2c33089-e7f0-48c5-bfaa-e531dff83833` still finished `SUCCEEDED` with empty output.
- Blockers: The published all-in-one Workflow API image-reference endpoint still does not expose outputs even though the direct Seedance image-reference API task works.
- Next step: Use the app-side direct `POST /v1/text_to_video` image-reference lane for the hackathon demo; keep endpoint `8ab20d96...` as a diagnostic checkpoint.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Split the image board from the hero MP4 route and published three image-board row endpoints: row 1 `f4ed6cf3-69b0-436b-a37c-82e1a7eeeb46`, row 2 `06a818f1-6dec-4cae-878d-ceeb6fbd5c2d`, and row 3 `fd051825-a295-4406-a80b-1fbfd8f8b7da`. Each keeps the 13 input/serial Combine/Claude planner contract, parses one group of three `image_reference_prompts`, generates three Nano Banana refs, exposes three `image` outputs, and removes final Seedance plus reference clips.
- Validation: Direct invocations `d99becc7-1da3-489a-a94e-c1bd4c693621`, `f7360924-0e1f-479d-a223-0d53ff901813`, and `dcfe5d44-e8f7-4bbf-9fdc-0da897b5f0ae` all completed `SUCCEEDED` with 3 image outputs each. `uv run python scripts/run_runway_image_board_rows.py --status ...` reports 9 total images without printing URLs. Hero endpoint `e4a221...` remains verified and returned a fresh MP4.
- Blockers: None for the separated nine-image board proof; it is not yet integrated into the web UI.
- Next step: Add a package-page image-board lane that can submit/check the three row workflows and present the nine reference images beside the hero MP4.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Newly published text-only fallback endpoint `9c0f1f38-e664-4b9e-9402-f2dae15b692b` matched the old successful graph shape but invocation `4732c4b5-f714-48bf-8b8c-a5d0ac5f96d9` still finished `SUCCEEDED` with no exposed outputs. Switched local `.env` to historically successful endpoint `e4a221ab-743d-45ac-bc47-633d66227614`, whose app invocation `de9c70e6-972a-44ca-ae16-119d3d1ab762` returned one MP4.
- Validation: `uv run python scripts/verify_runway_workflow_contract.py` passes against `e4a221...`; warnings note duplicated canvas defaults, but app submissions override all 13 inputs. Graph inspection confirms final Seedance video output is exposed.
- Blockers: Fresh local app invocation `414d3a5a-8554-4b8b-ae31-2b2853c6f920` succeeded with one MP4 output.
- Next step: Keep `e4a221...` as the stable hero endpoint and build the image board as a separate workflow lane.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Keyframe-only endpoint `8923373c-fee1-4506-94b5-b9b8bd13370a` crossed the old 72.5% wall and reached 80%, but invocation `f2071527-86b9-4471-81e3-ee769f20f051` finished `SUCCEEDED` with no exposed outputs. Published text-only fallback endpoint `9c0f1f38-e664-4b9e-9402-f2dae15b692b`, matching the previously proven serial Combine/Claude/refiner/final Seedance shape: 16 runnable nodes, no image refs or sidecars, final Seedance fed only by `textPrompt`, final `video` exposed, and `generateAudio` enabled.
- Validation: `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults` passed against `9c0f1f38...`; graph inspection confirmed final Seedance has only the refined prompt as input and exposes `video`.
- Blockers: Invocation `4732c4b5-f714-48bf-8b8c-a5d0ac5f96d9` finished `SUCCEEDED` with no exposed outputs.
- Next step: Superseded by known-good endpoint `e4a221ab-743d-45ac-bc47-633d66227614`.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Diagnosed the new `afd546...` stall at 72.5% as a graph-progress wall inside the nine-image Nano Banana reference board: the 40 runnable nodes break down so 72.5% equals 29/40, before the sidecar Seedance reference clips or final Seedance output should complete. Published keyframe-only endpoint `8923373c-fee1-4506-94b5-b9b8bd13370a`, which removes sidecar clips and seven of nine image refs, leaving final Seedance fed only by the refined prompt plus `Ref Image 01` as `firstFrame` and `Ref Image 09` as `lastFrame`.
- Validation: `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-keyframe-only` passed against `8923373c...`; VS Code diagnostics found no verifier errors.
- Blockers: Invocation `f2071527-86b9-4471-81e3-ee769f20f051` finished `SUCCEEDED` with no exposed outputs.
- Next step: Superseded by text-only endpoint `9c0f1f38-e664-4b9e-9402-f2dae15b692b`.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Diagnosed the sidecar-free stall at 87.5% as likely final Seedance `referenceVideos` routing mixed with `firstFrame`/`lastFrame` keyframes. Published endpoint `afd546a3-dbdb-4372-8aff-3a9c0e5282e8`, which keeps nine Nano Banana image refs and three Seedance reference clips, exposes the reference clips as sidecar outputs, disables final `referenceVideos`, and keeps final Seedance `generateAudio` enabled. This endpoint is now superseded by the keyframe-only fast path.
- Validation: `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-reference-board` passed against `afd546...`. `uv run pytest` passed with 21 tests. Started fixed live invocation `97703298-5d9b-4048-9ef4-b47050fed0a5`; first status was `RUNNING` at 30.0% with no outputs or failure.
- Blockers: Invocation `97703298-5d9b-4048-9ef4-b47050fed0a5` later stalled at 72.5%, likely inside the nine-image Nano Banana board.
- Next step: Superseded by keyframe-only endpoint `8923373c-fee1-4506-94b5-b9b8bd13370a`.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Started the first sidecar-free live workflow test from the local app route. Invocation `bfad2308-18e1-44d9-910e-f5ebafa8a39e` is running on endpoint `1827e99b-ea37-44f2-8525-45c5e299369d`. Added 20-second auto-refresh to the package page while workflow/direct Runway jobs are active so the progress UI can be watched without manual refresh clicks.
- Validation: `GET /package/episode_003/runway-status` returned HTTP 200, rendered the auto-refresh tag, and saved status `RUNNING` at 70.0% with no outputs or failure yet. `uv run pytest` passed with 21 tests.
- Blockers: This invocation later stalled at 87.5%, most likely at the final Seedance node after the three plain text-to-video reference clips completed.
- Next step: Superseded by keyframe-only endpoint `8923373c-fee1-4506-94b5-b9b8bd13370a`.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Added Runway progress telemetry to the package status UI. Workflow and direct generation state now store `progress`, the package page renders a progress bar and output media counts, and helper coverage verifies progress extraction plus media-type grouping.
- Validation: `uv run pytest` passed with 21 tests. VS Code diagnostics reported no errors for the edited app/schema/test files. Restarted the local app on `http://127.0.0.1:8002` and confirmed `episode_003` status renders `89.1%` plus `3 audios` for the still-running old invocation.
- Blockers: Invocation `974f5e16-aa0f-478b-ac82-56666d268b62` remains stuck at progress `0.8913043478260869` with 3 MP3 outputs, 0 MP4 outputs, 0 node errors, and no failure.
- Next step: Superseded by current keyframe-only endpoint `8923373c-fee1-4506-94b5-b9b8bd13370a`; keep old invocations as watch-only.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Published sidecar-free endpoint `1827e99b-ea37-44f2-8525-45c5e299369d`. It removes the three `audio_reference_prompts` parser nodes and three `eleven-text-to-sfx` nodes, keeps the nine Nano Banana Pro image refs and three Seedance reference clips, and leaves final Seedance `generateAudio` enabled. `.env` now points to this endpoint and the package page confirms it.
- Validation: Runway internal dynamic workflow validation returned `valid: true` for editor version 246 before publish. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-reference-board` passed against endpoint `1827e99b-ea37-44f2-8525-45c5e299369d`. `uv run pytest` passed with 19 tests.
- Blockers: No blocker for the sidecar-free endpoint contract. The previous parser-output-name endpoint `cfe53adb-2804-485d-adda-ae073626b0d0` is still running as invocation `974f5e16-aa0f-478b-ac82-56666d268b62` with 3 outputs and 0 node errors at last check, so final Seedance output/audio quality is not yet confirmed.
- Next step: Let invocation `974f5e16-aa0f-478b-ac82-56666d268b62` finish if possible, then inspect whether the final Seedance MP4 includes usable generated audio before deciding whether to keep sidecar audio disabled.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Tightened the nine-image board after manual inspection. The image parser handoffs are real in the graph: each `TCS Parser: image_reference_prompts[n]` feeds the matching `TCS Ref Image` node's `text_prompt`, and each `TCS Parser: audio_reference_prompts[n]` feeds the matching `TCS Audio Cue` node's `promptText`. Runway validation rejected hidden audio-reference input names on Seedance, confirming the current node exposes no direct audio-reference port. Fixed the final Seedance `referenceVideos` wiring by adding explicit indexes `0`, `1`, and `2`, then published endpoint `bfb8bc80-47c6-45bd-829d-b817414d10b9` and updated `.env` to use it.
- Validation: Runway internal dynamic workflow validation returns `valid: true` for editor version 237. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-reference-board` passed against endpoint `bfb8bc80-47c6-45bd-829d-b817414d10b9`. `uv run pytest` passed with 19 tests.
- Blockers: Seedance workflow nodes expose `generateAudio` but no audio asset/reference input. The audio cue nodes still generate sidecar refs from text prompts using the Runway sound effect contract (`eleven_text_to_sound_v2`).
- Next step: When ready to spend credits, run the full endpoint once and confirm the invocation returns all sidecar image/audio/reference clip assets plus the final hero clip.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Built and published the orderly nine-image reference board on top of the corrected input baseline. The new endpoint `d5e3926d-2ddd-40b0-894b-726780fcefdd` has nine `gemini-image-3-pro` image-reference nodes arranged as three triptychs, three `eleven-text-to-sfx` audio cue nodes aligned with those rows, and three four-second Seedance reference clips feeding the final Seedance hero clip. Updated `.env` to point at the new endpoint and extended `scripts/verify_runway_workflow_contract.py` with `--require-reference-board`.
- Validation: Runway dynamic workflow validation accepted the 61-node, 74-edge graph before save. `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults --require-reference-board` passed against endpoint `d5e3926d-2ddd-40b0-894b-726780fcefdd`. `uv run pytest` passed with 18 tests.
- Blockers: The current Seedance workflow node exposes image/video reference ports but no direct audio-reference input, so the three audio cues are generated as sidecars and their sound direction is folded into each reference-clip prompt.
- Next step: Run a paid endpoint invocation only when ready to test cost/latency for the full board, then inspect whether all sidecar assets and the final hero output expose cleanly.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Verified the TCS input-to-Combine-to-planner contract before starting the nine-image board. The published endpoint has 13 distinct input node IDs and the serial Combine chain correctly feeds the Claude planner, parser, refiner, final Seedance node, and sidecar proof clip. Added `scripts/verify_runway_workflow_contract.py` to make this check repeatable. Republished the corrected Runway editor canvas as endpoint `691b3f2b-720c-4b45-ade1-3190a45b11d5` and updated local `.env` to use it.
- Validation: `uv run python scripts/verify_runway_workflow_contract.py --strict-defaults` passed against endpoint `691b3f2b-720c-4b45-ade1-3190a45b11d5`.
- Blockers: None for the input/Combine/planner baseline. The next risky area is adding Nano Banana image nodes without reintroducing unsupported GPT Image 2 workflow nodes.
- Next step: Add the first Nano Banana image-reference checkpoint on top of endpoint `691b3f2b-720c-4b45-ade1-3190a45b11d5`, then republish and rerun the strict verifier before widening to all nine images.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Added the app-side direct Runway generation lane on package pages. The new state tracks Nano Banana image tasks separately from published workflow invocations, then advances a completed `1536:2752` image into direct `seedance2` image-to-video using the proven first-frame contract.
- Validation: `uv run pytest` passed with 18 tests.
- Blockers: Direct lane still runs as a two-step status refresh flow; a future polish pass can make the status polling more automatic.
- Next step: Try the package-page direct lane on a fresh episode when ready to spend another live Runway image/video pair, then fold the route into the demo script.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Continued the Nano Banana Pro integration using the Seedance guide. Added direct Runway client helpers/constants for `gemini_image3_pro` high-resolution image tasks and `seedance2` image-to-video first-frame handoff. Set the direct handoff default to `1536:2752`; `3072:5504` completed as a Nano Banana image task but exceeded Seedance's 16 MB raw PNG `promptImage` limit.
- Validation: `uv run pytest` passed with 14 tests; `uv run python scripts/agent_repo_audit.py` completed; VS Code diagnostics reported no errors; `git diff --check` reported only known CRLF normalization warnings. Live Nano Banana task `6abcc1e7-81ec-42fc-90e5-b0277e134d3f` fed Seedance task `83e7205d-7e4f-4f8c-81ad-50b963fc0f66`, which completed `SUCCEEDED` with one video output.
- Blockers: Published Workflow image-node routing still needs a Nano Banana-safe endpoint rebuild; max `3072:5504` direct images need resize/compression before raw Seedance handoff.
- Next step: Add a workflow checkpoint or app-side route that generates a `1536:2752` Nano Banana first frame, then submits it through the proven Seedance image-to-video path with creator approval.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Pivoted the hackathon image lane away from GPT Image 2 after endpoint `ec5e1e70-0406-41e2-9195-08ef5e32f7c4`, invocation `23af7906-76c5-448f-8884-a6357025d924`, reproduced `No model variant mapping for app node type: gpt-tidepool-alpha` even with one serially wired GPT Image node. Updated app defaults and docs to use Nano Banana Pro / Gemini 3 Pro Image (`gemini_image3_pro`) with Nano Banana / Gemini 2.5 Flash (`gemini_2.5_flash`) as the fast fallback, and added direct Runway `POST /v1/text_to_image` / `GET /v1/tasks/{id}` client helpers using Gemini's accepted portrait ratio `768:1344`.
- Validation: `uv run pytest` passed with 13 tests; `uv run python scripts/agent_repo_audit.py` completed; VS Code diagnostics reported no errors; `git diff --check` reported only known CRLF normalization warnings. Direct Nano Banana Pro task `8f46769b-92d3-4412-8c96-89d5d4445f25` completed `SUCCEEDED` with one image output after switching from invalid `1080:1920` to accepted `768:1344`.
- Blockers: Need a tiny first-frame/reference handoff proof before feeding Nano Banana image outputs into final Seedance.
- Next step: Use the successful Nano Banana output as a Seedance first-frame/reference input in a small checkpoint, then expand toward a nine-image board only after that one-image route works.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Inventoried the scaffold, added README, Runway resources, project inventory, and safe environment variable setup for Top Comment Studio.
- Validation: Ran `python scripts/agent_repo_audit.py`; confirmed `.env` and `AI_REPO_AUDIT.md` are ignored by git.
- Blockers: Dev/build/test commands cannot be verified until the MVP stack is chosen.
- Next step: Choose the MVP stack, then add and push the first commit to `TechmanStudios/top-comment-studio`.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Created the public GitHub repository `TechmanStudios/top-comment-studio` and verified the local `origin` remote points to it.
- Validation: `gh repo view TechmanStudios/top-comment-studio` reports visibility `PUBLIC`.
- Blockers: No repo-creation blocker remains.
- Next step: Create the initial commit and push when Bryan is ready.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Added `.gitignore` coverage for local browser cookies/session exports and documented Runway Workflows plus Developer Portal model shortcuts.
- Validation: `git check-ignore` confirms likely cookie/session/auth-state filenames are ignored.
- Blockers: No local cookie file was found inside the repo during scan.
- Next step: Design the first custom Runway Workflow chain for the comment-to-Short pipeline.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Documented where custom Runway Workflow API endpoints land for the Techman Studios organization.
- Validation: Confirmed the URL is recorded in `docs/RUNWAY_RESOURCES.md`.
- Blockers: None.
- Next step: After creating the first custom workflow, capture its endpoint name and expected inputs/outputs in the workflow design docs.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Completed a final setup-readiness pass and documented the recommended Python/FastAPI/uv next-phase plan.
- Validation: Repo status was clean before edits; setup gaps are now explicit in README, architecture, inventory, known issues, and next-phase plan.
- Blockers: The app is not runnable until the implementation scaffold is added.
- Next step: Add `pyproject.toml`, `src/top_comment_studio/`, first manual comment route, JSON chain storage, and a pytest smoke test.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Added the first runnable FastAPI scaffold with manual comment input, guardrail review, deterministic Shorts package generation, local JSON chain storage, sample data, and pytest smoke tests.
- Validation: `uv sync`, `uv run pytest`, app health check, and `python scripts/agent_repo_audit.py` passed.
- Blockers: Runway Workflow submission is still manual; no paid API calls are made by the scaffold.
- Next step: Create or choose the first Runway custom workflow endpoint and wire a creator-approved submit action.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Added the app-side creator-approved Runway workflow submit path, including preview payloads, workflow config placeholders, status refresh, persisted invocation state, mocked client tests, and workflow contract docs.
- Validation: `python scripts/agent_repo_audit.py`; `uv run pytest` passed with 6 tests.
- Blockers: Live Runway generation still needs the published `TCS Seedance Director v1` workflow UUID and node map from the Developer Portal.
- Next step: Build and publish the workflow in Runway, then paste `RUNWAY_WORKFLOW_ID` and `RUNWAY_WORKFLOW_NODE_MAP_JSON` into local `.env`.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Rebuilt the cleaned Runway canvas with the richer director prompt, a second JSON parser for the remaining image/reference-clip fields, one fresh GPT Image 2 node, and a final Seedance 2.0 node; published endpoint `8ae9c852-4319-417c-9d08-f389570b5db1` and pointed local `.env` at it.
- Validation: Inspected the published graph through the Runway API; the 13 TCS inputs remain exposed with stable node IDs, the final Seedance `video` output is exposed, and the GPT Image node has `taskType: workflow_gpt_image_2`. Restarted FastAPI on `http://127.0.0.1:8002`, submitted `episode_003` once with creator approval, and refreshed status for invocation `8b5d57dd-7469-4b19-b572-3cc732237110`. Updated the live Director System Prompt again so Claude returns raw JSON without code fences; the first Parse JSON node exposed extracted values for the new schema.
- Blockers: The invocation returned `SUCCEEDED` with an empty `output` object and a GPT Image runtime error: `No model variant mapping for app node type: gpt-tidepool-alpha`.
- Next step: Recheck the second JSON Parse node for `image_reference_prompts.8` and `reference_clip_plans.*.prompt`, then publish a tiny diagnostic endpoint with Combine Text directly feeding Seedance textPrompt and no image edge; if that produces video, keep GPT Image 2 out of the Workflow graph until Runway exposes an API-safe image node or move image generation to direct API calls.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Built and published `TCS Seedance Director v1` in Runway Workflows with 13 explicit app input nodes, a Combine Text director brief tree, Claude JSON planning, Parse JSON fan-out, GPT Image 2 references, Text to SFX sidecar cues, and a final Seedance 2.0 hero clip node.
- Validation: Published output-fixed 1080p endpoint UUID `961b51c3-6d75-408f-b98c-464728c829b4`; `uv run pytest` passed with 6 tests; `python scripts/agent_repo_audit.py` completed.
- Blockers: Local `.env` still needs the published workflow UUID and node map before the app can submit live Runway jobs.
- Next step: Add the documented `RUNWAY_WORKFLOW_ID` and `RUNWAY_WORKFLOW_NODE_MAP_JSON` to local `.env`, restart the app, and test one creator-approved submit.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Published and tested text-only diagnostic endpoint `4cec124c-3217-4435-844c-0b794dc2cdcc`; it removed GPT Image from the final branch but still returned `SUCCEEDED` with empty output. Published direct Seedance diagnostic endpoint `34abb3cb-1f88-4a2a-b5d4-3fc0888e9c36`, where `TCS Input: script` feeds Seedance `textPrompt` directly and only Seedance `video` is exposed. Removed the legacy `RUNWAYML_API_SECRET` variable from local `.env`; the app now relies on `RUNWAYML_HACKATHON_API_SECRET`.
- Validation: Inspected both published workflow graphs through `GET /v1/workflows/{id}`. Direct endpoint graph has 13 stable TCS inputs and a single Seedance video output; Seedance receives `0fb93ec3-f453-47bd-8e92-d1d4a6e6e815.prompt` directly. Submitted episode 3 to direct endpoint as invocation `e46ba302-ccde-4ff8-97fb-796b13e6de15`; first status was `RUNNING`.
- Blockers: Waiting for direct Seedance Workflow API invocation to complete; previous parsed endpoint still exposed no final output despite manual canvas Seedance succeeding.
- Next step: Refresh invocation `e46ba302-ccde-4ff8-97fb-796b13e6de15`; if it returns video, reintroduce the parser branch carefully, otherwise escalate as a published Workflow API output issue with a minimal Seedance-only repro.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Reduced the Runway canvas to a true two-node diagnostic: one `TCS Input: script` node feeding one Seedance 2.0 node. Published endpoint `45745fae-baed-498c-b84e-84c9ff5549bb` first with disconnected nodes still present; its invocation `4290417d-7633-457f-8651-6de272fc3a69` showed the Workflow API still executed disconnected Claude and failed on missing prompt. Deleted the disconnected nodes and published true minimal endpoint `5d1d6d5f-c194-4aaf-841a-bf68fa618425`.
- Validation: Inspected `5d1d6d5f-c194-4aaf-841a-bf68fa618425` through `GET /v1/workflows/{id}`; it has 2 nodes, 1 edge, exposed `script.prompt`, and exposed Seedance `video`. Submitted one-field payload directly via `RunwayClient` as invocation `ba15f8c4-8363-4a6d-b16f-a117daf3b605`; it completed `SUCCEEDED` and returned one Seedance MP4 URL with zero node errors. `uv run pytest` passed with 11 tests.
- Blockers: The minimal Seedance Workflow API path works; the remaining blocker is rebuilding the richer graph without disconnected/extra model nodes and without the GPT Image `gpt-tidepool-alpha` endpoint failure.
- Next step: Rebuild upward from the two-node base. First add the 13 app input text nodes only, keeping Seedance fed by `script`, publish/test. Then add one parser/planner stage, publish/test. Add GPT Image or reference clips only after their own tiny published endpoint proves API-safe execution.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Rebuilt upward from the successful two-node base by duplicating app input text nodes to restore the 13 logical app inputs while keeping only the original `script` node connected to Seedance. Published checkpoint endpoint `82d1f2da-0ed8-4bdc-8888-9c804852c2c1` and mapped local `.env` to all 13 exposed prompt nodes.
- Validation: `GET /v1/workflows/82d1f2da-0ed8-4bdc-8888-9c804852c2c1` reports 14 nodes, 1 edge, 13 exposed text `prompt` inputs, and exposed Seedance `video`. Submitted `episode_003` through the local app as invocation `86d47202-4abe-4a40-8833-fd96947349c9`; it completed `SUCCEEDED` with one Seedance MP4 output and zero node errors. `uv run pytest` passed with 11 tests; `uv run python scripts/agent_repo_audit.py` completed.
- Blockers: The 13-input checkpoint works. The duplicated input nodes are API-mapped by ID, but their visible Runway labels still need cleanup before a polished endpoint.
- Next step: Rename/recreate the 13 input nodes cleanly, then add the next single planner/parser stage and publish/test again before reintroducing GPT Image or reference-clip braiding.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Cleaned the Runway canvas around the working 13-input checkpoint: renamed all exposed app input nodes to their logical contract names, arranged them into non-overlapping metadata, audience-context, and creative-direction columns, and kept Seedance as the right-side generation stage. Published layout checkpoint endpoint `eee1e1d2-71e8-4cc5-a516-416ee71e1f89`.
- Validation: `GET /v1/workflows/eee1e1d2-71e8-4cc5-a516-416ee71e1f89` reports 14 nodes, 1 edge, 13 uniquely named exposed text `prompt` inputs, and exposed Seedance `video`. Submitted `episode_003` through the local app as invocation `54d26e50-af62-4f2e-b936-a37a08a8a15c`; it completed `SUCCEEDED` with one Seedance MP4 output and zero node errors. `uv run pytest` passed with 11 tests; `uv run python scripts/agent_repo_audit.py` completed.
- Blockers: The polished direct Seedance checkpoint works. The next risk is adding planner/parser nodes without reintroducing disconnected executable nodes or empty-output behavior.
- Next step: Add one planner/parser stage in its own grouped column, publish/test that checkpoint, then defer GPT Image/reference-clip braiding until tiny image/reference endpoints prove API-safe execution.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Added the next incremental Runway stage: hidden `TCS Planner: system_prompt` Text node -> `TCS Planner: Claude JSON` -> `TCS Parser: seedance_prompt` -> final Seedance 2.0. Kept the 13 exposed app inputs and local node map unchanged, hid the internal system prompt on publish, and pointed local `.env` at endpoint `07eab094-6c6a-46a4-9dfb-963d97a293f5`.
- Validation: Draft and published graphs both report 17 nodes and 4 edges; the canvas collision check found zero overlaps. `GET /v1/workflows/07eab094-6c6a-46a4-9dfb-963d97a293f5` shows only the 13 app text prompts plus Seedance `video` exposed. Restarted FastAPI on port 8002 and submitted `episode_003` as invocation `e1888b11-d1d5-4078-af20-c583746bad48`; it completed `SUCCEEDED` with one Seedance MP4 output. `uv run pytest` passed with 11 tests; `uv run python scripts/agent_repo_audit.py` completed.
- Blockers: No blocker remains for the Claude -> Parse JSON -> Seedance checkpoint. GPT text refinement is still unresolved because the Runway node picker showed GPT Image nodes but no GPT text/LLM node.
- Next step: Add one GPT/text refinement layer outside the fragile image branch, either app-side/direct API or with a newly available Runway text LLM node, then publish/test before adding GPT Image or reference clips.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Replaced the requested text-refinement layer with a Runway-native Claude text node, restored all 13 app inputs into the planner through Runway Combine Text nodes, and rewired the Combine layer as a single serial chain after the initial parallel fan-in endpoint hit scheduler errors.
- Validation: Published serial endpoint `e4a221ab-743d-45ac-bc47-633d66227614`; `GET /v1/workflows/e4a221ab-743d-45ac-bc47-633d66227614` reports 31 nodes, 30 edges, 12 `text-concat` nodes, 2 Claude nodes, 13 exposed app inputs, and one exposed Seedance output. Canvas collision check found zero overlaps. Restarted FastAPI on port 8002, submitted `episode_003` as invocation `de9c70e6-972a-44ca-ae16-119d3d1ab762`, and refreshed it to `SUCCEEDED` with one Seedance MP4 output and no node errors. `uv run pytest` passed with 11 tests; `uv run python scripts/agent_repo_audit.py` completed; VS Code diagnostics reported no errors; `git diff --check` only reported existing CRLF warnings.
- Blockers: No blocker remains for the serial Combine -> Claude planner -> Parse JSON -> Claude refiner -> Seedance checkpoint. GPT Image/reference-clip branches remain deferred until tiny published endpoints prove API-safe execution.
- Next step: Add the first tiny reference-asset endpoint, preferably one API-safe image or one short Seedance reference clip, then publish/test before routing references into the final hero clip.
```

```text
2026-05-10 — GitHub Copilot:
- Summary: Added the first reference-asset proof as a second 5-second Seedance 2.0 sidecar node, fed by the existing Claude refiner prompt and exposed alongside the final hero Seedance output.
- Validation: Published endpoint `b9beb013-0fe5-4f20-b244-a39b788ae95d`; `GET /v1/workflows/b9beb013-0fe5-4f20-b244-a39b788ae95d` reports 32 nodes, 31 edges, 12 `text-concat` nodes, 2 Claude nodes, 2 Seedance nodes, 13 exposed app inputs, and 2 exposed video outputs. Canvas collision check found zero overlaps. Restarted FastAPI on port 8002, submitted `episode_003` as invocation `06ee71a5-3e6e-4b36-ade3-7d199bada83a`, and refreshed it to `SUCCEEDED` with two Seedance MP4 outputs and no node errors. `uv run pytest` passed with 11 tests; `uv run python scripts/agent_repo_audit.py` completed; VS Code diagnostics reported no errors; `git diff --check` only reported existing CRLF warnings.
- Blockers: No blocker remains for a sidecar Seedance reference clip that runs independently. Later tests showed final `referenceVideos` can stall when mixed with first/last keyframes.
- Next step: Keep generated reference clips exposed as sidecar outputs unless a smaller future endpoint proves `referenceVideos` can be used without stalling.
```
