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

Decision: Store the real Runway API secret only in local `.env` as `RUNWAYML_API_SECRET`; keep `.env.example` placeholder-only.

Why: The project is being prepared for a public repository and must not publish live credentials.

Alternatives considered: Leaving the key in `helpful.txt` for convenience.

Tradeoffs: Contributors must copy or request the real secret locally, but the repo remains safe to publish.

Follow-up: Rotate the key if it was ever committed or shared outside the local machine.

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

Follow-up: Confirm exact endpoint model identifiers from the Runway workflow registry after the custom workflow is created.
