# Agent Prompt Pack

Copy these prompts into Codex, VSCode agents, Copilot Chat, or another coding assistant.

## 1. Initial Repo Setup

```text
Read AGENTS.md, HACKATHON_AGENT_SETUP.md, START_HERE_FOR_AI.md, and PROJECT_BRIEF.md.

Inspect the repository and identify the stack, package manager, setup command, dev command, build command, test command, and required environment variables.

Do not make code changes yet. First summarize what you found and propose the smallest safe setup changes.
```

## 2. Make the Repo Runnable

```text
Use the existing project conventions. Make the smallest changes needed so a fresh clone can install dependencies, create a .env file from .env.example, and run the app locally.

Update README.md with exact commands. Add or update .env.example using placeholders only. Do not commit secrets.

Run available validation commands and report results.
```

## 3. Implement MVP Feature

```text
Read PROJECT_BRIEF.md and TASKS.md.

Implement the smallest end-to-end version of the top-priority MVP feature. Prefer simple, readable code. Avoid broad refactors.

Add or update a minimal test or smoke check if practical. Update TASKS.md and KNOWN_ISSUES.md when done.
```

## 4. Fix Build/Test Failures

```text
Run the documented build and test commands. Fix setup-related failures first. Do not disable tests to force success.

If a failure is deeper than setup, document it in KNOWN_ISSUES.md with reproduction steps and the likely next fix.
```

## 5. Prepare Demo

```text
Read docs/DEMO_SCRIPT.md and PROJECT_BRIEF.md.

Make the app demo-friendly. Add sample data if needed, but do not include private data or real secrets.

Prioritize the happy path, clear error messages, and a smooth local run command.
```

## 6. Final Handoff

```text
Produce a final handoff with:

Summary:
Validation:
Files changed:
Known issues:
Next best step:

Update TASKS.md, DECISIONS.md, or KNOWN_ISSUES.md if anything important changed.
```
