# GitHub Copilot Instructions

Follow the repo-level guidance in `AGENTS.md`.

## Hackathon Bias

Favor simple, demoable, working code over broad architectural refactors.

## When Editing

- Preserve existing style and framework conventions.
- Prefer small diffs.
- Add comments only where they clarify non-obvious logic.
- Do not invent secrets or real credentials.
- Update docs when setup commands or environment variables change.

## When Unsure

Inspect the repository before guessing.

If there are multiple valid options, choose the least invasive option and document the tradeoff in `DECISIONS.md`.

## Validation

After meaningful changes, suggest or run the most relevant command:

```bash
npm run build
npm test
pnpm build
pnpm test
pytest
python -m pytest
```
