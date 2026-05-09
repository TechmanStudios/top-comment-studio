# Start Here for AI Agents

You are helping prepare this repository for a hackathon.

## Immediate Goal

Make the project easy for Bryan and collaborators to run, modify, and demo.

## First Message to Bryan

After inspecting the repo, report:

```text
I found:
- Stack:
- Package manager:
- App entry point:
- Setup command:
- Dev command:
- Build command:
- Test command:
- Missing/unclear items:
```

Then propose the smallest next step.

## First Commands to Try

From the repo root:

```bash
ls
python scripts/agent_repo_audit.py
```

Then inspect files such as:

```bash
README.md
package.json
pyproject.toml
requirements.txt
Dockerfile
docker-compose.yml
.env.example
```

## Build Strategy

For hackathon work, use this order:

1. Get the repo running locally.
2. Add `.env.example`.
3. Add or repair README setup instructions.
4. Add minimal tests or smoke checks.
5. Implement MVP features.
6. Polish only what affects the demo.

## Do Not Guess

If a command is unknown, inspect the repo first.

If an environment variable is unknown, search the codebase and add a placeholder to `.env.example`.

If there are multiple possible frameworks, identify evidence before changing files.

## End State

A new contributor should be able to understand the repo in five minutes and run it in fifteen.
