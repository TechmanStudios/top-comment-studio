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
