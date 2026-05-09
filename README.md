# Top Comment Studio

Top Comment Studio is a weekend hackathon project for turning audience comments into the next YouTube Shorts production package. The MVP keeps Bryan in the review loop: select or paste a strong audience comment, apply safety and brand guardrails, generate a short-form script and Runway-ready media prompts, then log the next link in the series chain.

## Current Status

This repository now has the first runnable FastAPI scaffold for the manual comment-to-Shorts-package flow. The app generates deterministic draft packages locally and does not call paid Runway or LLM APIs yet.

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

## Environment Variables

| Name | Purpose |
|---|---|
| `APP_ENV` | Local runtime mode. |
| `LOG_LEVEL` | Development logging level. |
| `APP_NAME` | Human-readable app name. |
| `RUNWAYML_API_SECRET` | Server-side Runway API bearer token. |
| `RUNWAYML_API_BASE_URL` | Runway API base URL. |
| `RUNWAYML_API_VERSION` | Runway API version header. |
| `RUNWAY_WORKFLOW_REGISTRY_URL` | Developer Portal page where custom workflow endpoints appear. |
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
- [docs/PROJECT_INVENTORY.md](docs/PROJECT_INVENTORY.md)
- [docs/NEXT_PHASE_BUILD_PLAN.md](docs/NEXT_PHASE_BUILD_PLAN.md)

## Validation

The repo includes a lightweight audit script:

```powershell
python scripts/agent_repo_audit.py
```

The audit should now detect the Python stack and `pyproject.toml`.

## Next Best Build Step

The first vertical slice is in place. The next build step is to connect the deterministic package output to a Runway Workflow endpoint behind explicit creator approval:

1. Capture the custom workflow endpoint name.
2. Map the package fields to workflow inputs.
3. Add a dry-run preview before any paid generation.
4. Add an explicit creator-approved Runway submit action.
