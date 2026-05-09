# Hackathon Repo Setup Instructions for Coding Agents

## Mission

Prepare this repository so a developer can clone it, install dependencies, run the app, run tests, and start building hackathon features quickly. Prioritize a clean, reproducible local setup over deep refactors.

This file is intended for coding agents such as Codex, VSCode agents, GitHub Copilot agents, or human contributors.

---

## Operating Rules

1. **Do not rewrite the whole project.** Make the smallest practical changes needed to get the repo running.
2. **Preserve existing architecture.** Improve setup, docs, scripts, and obvious broken paths only.
3. **Prefer reproducibility.** Every setup step should be documented and runnable from a fresh clone.
4. **Leave clear notes.** If something cannot be fixed safely, add a concise TODO with the reason.
5. **Do not commit secrets.** Never create or expose real API keys, tokens, credentials, private URLs, or `.env` values.
6. **Assume hackathon speed.** Favor simple, understandable solutions over perfect abstractions.

---

## First Pass: Inspect the Repo

Before changing files, identify:

- Primary language and framework.
- Package manager.
- App entry point.
- Test command, if any.
- Build command, if any.
- Required environment variables.
- Existing README/setup docs.
- Any obvious missing config files.

Look for files such as:

```text
README.md
package.json
pnpm-lock.yaml
yarn.lock
requirements.txt
pyproject.toml
uv.lock
Pipfile
Dockerfile
docker-compose.yml
.env.example
Makefile
```

---

## Setup Tasks

Complete as many of these as are relevant:

### 1. Create or update `.env.example`

Add placeholder values only:

```bash
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=your_database_url_here
APP_ENV=development
```

Only include variables actually used by the repo.

### 2. Create or update setup instructions

Update `README.md` with a short **Local Setup** section:

```bash
git clone <repo-url>
cd <repo-name>
cp .env.example .env
# install dependencies
# run the app
# run tests
```

Use the real commands discovered from the repo.

### 3. Add helper scripts if missing

If appropriate, add simple scripts for common commands.

For JavaScript/TypeScript projects, prefer `package.json` scripts:

```json
{
  "scripts": {
    "dev": "...",
    "build": "...",
    "test": "...",
    "lint": "..."
  }
}
```

For Python projects, prefer a `Makefile` or documented commands:

```makefile
install:
	pip install -r requirements.txt

dev:
	python app.py

test:
	pytest
```

### 4. Verify dependency installation

Use the package manager already implied by the repo:

- `pnpm install` if `pnpm-lock.yaml` exists.
- `yarn install` if `yarn.lock` exists.
- `npm install` if `package-lock.json` or only `package.json` exists.
- `uv sync` if `uv.lock` or `pyproject.toml` indicates `uv`.
- `pip install -r requirements.txt` for simple Python repos.

Do not switch package managers unless there is a strong reason.

### 5. Run validation commands

Run the commands that exist or were added:

```bash
# examples only
npm run build
npm test
npm run lint
pytest
python -m pytest
```

If a command fails, fix obvious setup-related issues. If it is a deeper app bug, document it under **Known Issues**.

---

## Preferred Output

When finished, provide a concise summary with:

```text
Completed:
- Updated README local setup instructions.
- Added .env.example.
- Added dev/test scripts.
- Verified install command.

Validation:
- install: passed
- build: passed
- tests: failed — missing DATABASE_URL; documented in README

Files changed:
- README.md
- .env.example
- package.json
```

---

## Definition of Done

The repo is hackathon-ready when a new contributor can:

1. Clone the repo.
2. Install dependencies.
3. Create a local `.env` from `.env.example`.
4. Run the app locally.
5. Run at least one validation command.
6. Understand any known setup limitations within five minutes.

---

## Agent Reminder

Optimize for momentum. The goal is not to perfect the codebase; the goal is to make the repo easy to start, easy to run, and safe for fast hackathon iteration.
