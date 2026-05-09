# Top Comment Studio

Top Comment Studio is a weekend hackathon project for turning audience comments into the next YouTube Shorts production package. The MVP keeps Bryan in the review loop: select or paste a strong audience comment, apply safety and brand guardrails, generate a short-form script and Runway-ready media prompts, then log the next link in the series chain.

## Current Status

This repository is in project setup mode. It currently contains planning docs, guardrails, prompt templates, YouTube notes, and agent workflow instructions. There is not yet an app framework, package manifest, build script, or test command.

## Local Setup

```powershell
git clone https://github.com/TechmanStudios/top-comment-studio.git
cd top-comment-studio
Copy-Item .env.example .env
```

Fill in local values in `.env`. Never commit `.env` or real credentials.

## Environment Variables

| Name | Purpose |
|---|---|
| `APP_ENV` | Local runtime mode. |
| `LOG_LEVEL` | Development logging level. |
| `APP_NAME` | Human-readable app name. |
| `RUNWAYML_API_SECRET` | Server-side Runway API bearer token. |
| `RUNWAYML_API_BASE_URL` | Runway API base URL. |
| `RUNWAYML_API_VERSION` | Runway API version header. |
| `OPENAI_API_KEY` | Optional LLM provider key for future script/prompt generation. |
| `DATABASE_URL` | Optional storage backend once the app needs persistent state. |
| `PORT` | Local web server port once an app exists. |
| `HOST` | Local web server host once an app exists. |
| `NEXT_PUBLIC_APP_URL` | Public app URL for a future web frontend. |

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

At the moment, the audit correctly reports that no app stack, package manifest, entry point, build command, dev command, or test command has been implemented yet.

## Next Best Build Step

Use the recommended Python/FastAPI plan in [docs/NEXT_PHASE_BUILD_PLAN.md](docs/NEXT_PHASE_BUILD_PLAN.md), then add the smallest runnable vertical slice:

1. Manual comment input.
2. Guardrail check.
3. Generated Short package.
4. Series-chain record.
5. Exportable Runway prompt package.
