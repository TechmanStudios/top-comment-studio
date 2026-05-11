# Top Comment Studio

Top Comment Studio is a weekend hackathon project for turning audience comments into the next YouTube Shorts production package. The MVP keeps Bryan in the review loop: select or paste a strong audience comment, apply safety and brand guardrails, generate a short-form script and Runway-ready media prompts, then log the next link in the series chain.

## Current Status

This repository now has a runnable FastAPI scaffold for the manual comment-to-Shorts-package flow, plus creator-approved Runway handoff paths. The current hackathon lane converts the audience signal into a unified Gen/Veo audio-video director packet, uses Nano Banana Pro / Gemini 3 Pro Image (`gemini_image3_pro`) for the reference board, uses Gen-4.5 (`gen4.5`) for silent cinematic shot studies, and uses Veo 3.1 (`veo3.1`) for the final sound-enabled video.

## Local Setup

```powershell
git clone https://github.com/TechmanStudios/top-comment-studio.git
cd top-comment-studio
Copy-Item .env.example .env
uv sync
```

Fill in local values in `.env`. Never commit `.env` or real credentials.

## Run The App

```powershell
uv run uvicorn top_comment_studio.app:app --reload
```

Then open http://127.0.0.1:8000.

## Run Tests

```powershell
uv run pytest
```

## Runway Workflow Submit

The app now includes a dry-run preview and explicit creator-approved submit path for the first published Runway workflow. Until the workflow is created and published in Runway, the package page will show configuration blockers instead of calling the API.

For standalone image generation, the Runway client supports `POST /v1/text_to_image` with Nano Banana Pro (`gemini_image3_pro`) as the default image model and Nano Banana / Gemini 2.5 Flash (`gemini_2.5_flash`) as the fast fallback. The direct Nano Banana Pro path defaults to the high-resolution portrait ratio `1536:2752`; use `3072:5504` for max-quality previsuals or `768:1344` for quick proofs. The app keeps `1080:1920` as the logical Shorts aspect. Use the returned task id with `GET /v1/tasks/{id}`.

For the one-image cinematic proof, the package page includes a separate creator-approved direct generation lane. It starts a Nano Banana Pro first-frame task, then a status refresh advances the completed image into direct `POST /v1/image_to_video` with `gen4.5`, passing the Nano Banana output URL as the `promptImage` first frame and using vertical `720:1280`.

For the final video, generate and refresh all three Nano Banana board rows first. The final-video button submits Veo 3.1 image-to-video with the board's first hero image as the single public-API prompt image, while the prompt carries the unified AV director packet and the nine-image board plan. Veo 3.1 is the final adapter because the demo output needs native sound.

Required local values after publishing a `TCS Gen/Veo Director v2` workflow or compatible board-row workflows:

```powershell
RUNWAYML_HACKATHON_API_SECRET=your_real_hackathon_secret
RUNWAY_WORKFLOW_ID=published_workflow_uuid
RUNWAY_WORKFLOW_NODE_MAP_JSON={"av_director_packet":{"node_id":"node-uuid","output_key":"prompt"}}
```

The node map must include every logical input listed in [docs/RUNWAY_RESOURCES.md](docs/RUNWAY_RESOURCES.md). The submit button still requires an explicit creator approval checkbox before any paid Runway generation request is sent.

## Environment Variables

| Name | Purpose |
|---|---|
| `APP_ENV` | Local runtime mode. |
| `LOG_LEVEL` | Development logging level. |
| `APP_NAME` | Human-readable app name. |
| `RUNWAYML_HACKATHON_API_SECRET` | Preferred server-side Runway API bearer token for hackathon runs. |
| `RUNWAYML_API_BASE_URL` | Runway API base URL. |
| `RUNWAYML_API_VERSION` | Runway API version header. |
| `RUNWAY_WORKFLOW_REGISTRY_URL` | Developer Portal page where custom workflow endpoints appear. |
| `RUNWAY_WORKFLOW_ID` | Published Runway workflow UUID for the creator-approved submit action. |
| `RUNWAY_WORKFLOW_NAME` | Human-readable workflow name shown in the local UI. |
| `RUNWAY_WORKFLOW_NODE_MAP_JSON` | JSON mapping from logical app inputs to published workflow node IDs/output keys. |
| `OPENAI_API_KEY` | Optional LLM provider key for future script/prompt generation. |
| `DATABASE_URL` | Optional storage backend once the app needs persistent state. |
| `PORT` | Local web server port once an app exists. |
| `HOST` | Local web server host once an app exists. |
| `NEXT_PUBLIC_APP_URL` | Public app URL for a future web frontend. |
| `TOP_COMMENT_STUDIO_DATA_DIR` | Local JSON storage root for generated chain records. |

## Useful Docs

Start with these files:

- [START_HERE_FOR_AI.md](START_HERE_FOR_AI.md)
- [PROJECT_BRIEF.md](PROJECT_BRIEF.md)
- [MVP_SPEC.md](MVP_SPEC.md)
- [GUARDRAILS.md](GUARDRAILS.md)
- [COMMENT_SELECTION_POLICY.md](COMMENT_SELECTION_POLICY.md)
- [docs/RUNWAY_RESOURCES.md](docs/RUNWAY_RESOURCES.md)
- [docs/RUNWAY_WORKFLOW_BUILD_GUIDE.md](docs/RUNWAY_WORKFLOW_BUILD_GUIDE.md)
- [docs/PROJECT_INVENTORY.md](docs/PROJECT_INVENTORY.md)
- [docs/NEXT_PHASE_BUILD_PLAN.md](docs/NEXT_PHASE_BUILD_PLAN.md)

## Validation

The repo includes a lightweight audit script:

```powershell
python scripts/agent_repo_audit.py
```

The audit should now detect the Python stack and `pyproject.toml`.

## Next Best Build Step

The first vertical slice, local approval gate, and Runway handoff lanes are in place. The next build step is to configure the local app and run the creator-approved live submit path:

1. Add the current board-row workflow IDs and `RUNWAY_WORKFLOW_NODE_MAP_JSON` from [docs/RUNWAY_WORKFLOW_BUILD_GUIDE.md](docs/RUNWAY_WORKFLOW_BUILD_GUIDE.md) to local `.env`.
2. Restart the FastAPI app so settings reload.
3. Open a package page, generate the nine-image board, refresh until the rows finish, then submit the Veo 3.1 final video after creator approval.
4. Confirm whether Runway exposes a public Precision v2 upscaler endpoint before adding an automated upscaling step.
