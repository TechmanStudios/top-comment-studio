# AI Collaboration Workflow

This repo is designed to be worked on by Bryan plus AI coding agents.

## How to Give Agents Work

Use small, concrete asks:

```text
Read AGENTS.md and TASKS.md. Complete the first todo under Setup. Make the smallest safe changes. Run validation and update the task status.
```

Better than:

```text
Fix everything.
```

## Good Agent Tasks

- Add `.env.example`.
- Update README setup steps.
- Add missing npm scripts.
- Fix one failing test.
- Implement one route or component.
- Add a smoke test.
- Write a demo script.
- Document known issues.

## Risky Agent Tasks

Use extra care with:

- Large refactors.
- Database migrations.
- Auth changes.
- Deployment config.
- Payment flows.
- Secret handling.
- Removing files.

## Review Checklist

Before accepting agent changes:

- [ ] Did it keep the project runnable?
- [ ] Did it avoid secrets?
- [ ] Did it use the existing stack?
- [ ] Did it run validation?
- [ ] Did it update docs/tasks/issues?
- [ ] Is the diff small enough to understand?

## Suggested Human + Agent Loop

1. Bryan gives one focused task.
2. Agent inspects relevant files.
3. Agent proposes a short plan.
4. Agent edits.
5. Agent validates.
6. Bryan reviews the diff.
7. Agent updates task/issue docs.
