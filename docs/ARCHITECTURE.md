# Architecture

Keep this document current as the hackathon project evolves.

## System Overview

Top Comment Studio is a creator-facing workflow tool that turns an audience comment into a safe, reviewable YouTube Shorts production package. The MVP starts with manual comment input, applies guardrails, generates a creative interpretation plus script/prompts, logs the episode chain locally, and prepares a Runway-ready prompt or workflow handoff for creator approval.

## Main Components

| Component | Responsibility | Location |
|---|---|---|
| Creator UI | Manual comment input, review, and package display | `src/top_comment_studio/templates/` once implemented |
| Backend | FastAPI routes, orchestration, validation | `src/top_comment_studio/` once implemented |
| Domain Core | Guardrail review, creative interpretation, package generation | `src/top_comment_studio/` once implemented |
| Storage | Local JSON chain records and generated packages | `data/` once implemented |
| Runway Layer | Server-side Runway API and workflow endpoint calls | `src/top_comment_studio/runway/` once implemented |
| Auth | No app auth for MVP; local secrets only through `.env` | `.env`, `.env.example` |

## Data Flow

```text
User
  -> UI
  -> FastAPI route
  -> guardrail review
  -> creative package generator
  -> local chain storage
  -> optional Runway workflow/API handoff
  -> creator review response
```

## Important Files

| File/Folder | Purpose |
|---|---|
| `README.md` | Local setup and contributor instructions |
| `.env.example` | Safe placeholder environment variables |
| `AGENTS.md` | AI agent operating instructions |
| `TASKS.md` | Hackathon task board |
| `KNOWN_ISSUES.md` | Current issues and limitations |
| `docs/RUNWAY_RESOURCES.md` | Runway docs, model catalog, workflow endpoint registry |
| `docs/NEXT_PHASE_BUILD_PLAN.md` | Implementation handoff for the first runnable slice |

## AI Integration Notes

Provider:

- Runway API for media generation and custom workflow endpoints.
- Optional LLM provider for copy/script generation after deterministic templates work.

Model(s):

- Runway custom workflows from the Techman Studios workflow endpoint registry.
- Candidate media models: Gen-4.5, Gen-4 Image/Turbo, Seedance 2, Veo 3/3.1, ElevenLabs audio tools.

Prompt locations:

- `PROMPT_TEMPLATES.md`
- `prompts/agent_prompts.md`
- Future app prompt helpers under `src/top_comment_studio/`.

Safety/validation:

- `GUARDRAILS.md`
- `COMMENT_SELECTION_POLICY.md`
- Future Pydantic schemas and pytest smoke tests.

## Deployment Notes

Target platform:

- Local demo first.
- Deploy target to be selected after the MVP app route exists.

Required environment variables:

- `RUNWAYML_API_SECRET`
- `RUNWAYML_API_BASE_URL`
- `RUNWAYML_API_VERSION`
- Optional: `OPENAI_API_KEY`, `DATABASE_URL`, `PORT`, `HOST`, `NEXT_PUBLIC_APP_URL`

Build command:

- None yet. Add once the app scaffold exists.

Start command:

- Planned: `uv run uvicorn top_comment_studio.app:app --reload`

## Open Questions

- [ ] Confirm whether `uv` is acceptable as the package manager for the first Python scaffold.
- [ ] Decide whether the first demo calls Runway directly or exports prompts for manual Runway workflow execution.
- [ ] Choose the first custom Runway Workflow template to clone or build from scratch.
