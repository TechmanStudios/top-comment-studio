# Top Comment Studio

Top Comment Studio is a weekend hackathon project for turning audience comments into the next YouTube Shorts production package. The MVP keeps Bryan in the review loop: select or paste a strong audience comment, apply safety and brand guardrails, generate a short-form script and Runway-ready media prompts, then log the next link in the series chain.

## Current Status

This repository now has a runnable FastAPI demo flow for turning one editable audience comment into a creator-approved Runway render. The judge-facing path keeps Director Controls visible but locked, builds the Shorts package server-side, and submits the paid-proven v66 Gen/Veo workflow with one `Generate render` action. The package page then acts as the render monitor until the final MP4 is ready.

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

## Live Deployment

GitHub Pages can host a static project page, but it cannot run this FastAPI app or keep the Runway API secret server-side. For the live judging URL, deploy the app to a server-backed Python or Docker host, then point a Techman Studios subdomain at that host.

Current live judge URL:

```text
https://top-comment-studio.onrender.com/
```

The repo includes a root [render.yaml](render.yaml) Blueprint for Render. See [docs/LIVE_DEPLOYMENT.md](docs/LIVE_DEPLOYMENT.md) for the recommended Render setup, required environment variables, DNS notes, and secret-handling checklist.

## Runway Workflow Submit

The checked-in example configuration points to the current paid-proven v66 workflow endpoint, `c1b49d17-c80f-4705-b0e6-86c89a070464`, with its ten TCS input node mappings. The v66 graph uses the Gen/Veo continuity core, Nano Banana Pro / Gemini 3 Pro Image frame generation, photo-enhanced storyboard frames, Veo 3.1 keyframe segments, native audio, and a final 1080x1920 stitched MP4 output.

The intake page's `Generate render` action is the explicit creator-approved paid-generation action. It creates the package and submits the configured workflow in one step. The package page then auto-refreshes the workflow status until Runway returns the MP4, and `Open video` points at the newest workflow output.

Add your local Runway secret before submitting paid generations. Until the workflow and secret are configured, the render page shows configuration blockers instead of calling the API.

Required local values after publishing a replacement `TCS Gen/Veo Director v2` workflow:

```powershell
RUNWAYML_HACKATHON_API_SECRET=your_real_hackathon_secret
RUNWAY_WORKFLOW_ID=published_workflow_uuid
RUNWAY_WORKFLOW_NODE_MAP_JSON={"av_director_packet":{"node_id":"node-uuid","output_key":"prompt"}}
```

The node map must include every logical input listed in [docs/RUNWAY_RESOURCES.md](docs/RUNWAY_RESOURCES.md).

The UI does not expose a duration field. The app sends the v66-proven `duration_seconds=4` workflow input, which corresponds to the four 4-second Veo segments stitched into the final short.

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

- [docs/LIVE_DEPLOYMENT.md](docs/LIVE_DEPLOYMENT.md)

## Validation

The repo includes a lightweight audit script:

```powershell
python scripts/agent_repo_audit.py
```

The audit should now detect the Python stack and `pyproject.toml`.

## Next Best Build Step

The first vertical slice, locked demo controls, live Render deployment, and paid-proven v66 workflow path are in place. The next best step is final demo rehearsal:

1. Open `https://top-comment-studio.onrender.com/`.
2. Leave the default audience signal or edit only the selected audience comment.
3. Click `Generate render` only when ready to spend Runway credits.
4. Let the render page auto-refresh until `Render ready`, then use `Open video` for the MP4.
5. Defer the custom domain and any automated upscaling until after final submission unless they become required polish.
