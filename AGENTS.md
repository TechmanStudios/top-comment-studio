# AGENTS.md

Universal instructions for AI coding agents working in this repository.

Read this file before making changes. Also read `HACKATHON_AGENT_SETUP.md` if it exists.

## Project Mode

This repository is being prepared for a hackathon. Optimize for a working, demoable MVP with clear setup instructions.

The goal is not to over-engineer the system. The goal is to make the repo easy to run, easy to modify, and easy to demo.

## Agent Priorities

1. Keep the app runnable.
2. Make small, reviewable changes.
3. Preserve the existing architecture unless Bryan explicitly asks for a redesign.
4. Prefer clear documentation over cleverness.
5. Add validation commands whenever possible.
6. Never commit secrets, API keys, private tokens, or real credentials.
7. Leave a useful handoff note after meaningful work.

## Required First Steps

Before editing code:

1. Inspect the repo structure.
2. Identify the framework, runtime, package manager, and app entry point.
3. Read any existing README, docs, config files, and package manifests.
4. Run `python scripts/agent_repo_audit.py` if available.
5. Summarize what you found before making major changes.

## Safe File Changes

Agents may create or update:

- `README.md`
- `.env.example`
- `docs/*`
- `.github/*`
- `.vscode/*`
- tests
- setup scripts
- small source fixes needed to make setup/build/test work

Avoid large rewrites unless Bryan asks for them.

## Forbidden Actions

Do not:

- Delete large directories without explicit permission.
- Replace the framework without explicit permission.
- Add real secrets.
- Disable tests to make a build appear successful.
- Hide errors.
- Introduce paid external services unless they are already part of the plan.
- Make destructive git operations such as `git reset --hard`, `git clean -fd`, or force-push.

## Preferred Workflow

Use this loop:

1. Inspect.
2. Plan.
3. Make the smallest useful change.
4. Run validation.
5. Document what changed.
6. Update `TASKS.md`, `DECISIONS.md`, or `KNOWN_ISSUES.md` if relevant.

## Validation Expectations

Run the best available commands for the repo.

Common examples:

```bash
npm run lint
npm run test
npm run build
pnpm lint
pnpm test
pnpm build
pytest
python -m pytest
docker compose up --build
```

If commands are missing, document that clearly and suggest minimal additions.

## Handoff Format

At the end of work, provide:

```text
Summary:
- What changed.

Validation:
- Command: result
- Command: result

Files changed:
- path/to/file

Known issues:
- Anything still blocked or uncertain.

Next best step:
- One specific recommended action.
```

## Style Preference

Keep implementation practical, modern, and understandable. Bryan prefers Python for new scaffolds unless the repository clearly uses another stack.

Use straightforward names and avoid unnecessary abstractions.

## Additional Instructions 
Read AI_YOUTUBE_PROJECT_PHILOSOPHY.md before designing features. Preserve the Audience-in-the-Loop mechanic and short-form-first MVP direction.