# Hackathon Tasks

Use this as the shared task board for humans and AI agents.

## Status Legend

- `todo`
- `doing`
- `blocked`
- `done`

## Setup

| Status | Task | Notes |
|---|---|---|
| done | Identify stack and package manager | No app stack or package manager selected yet |
| blocked | Verify local install command | Blocked until stack is selected |
| blocked | Verify dev command | Blocked until app entry point exists |
| blocked | Verify build command | Blocked until package manifest exists |
| blocked | Verify test command | Blocked until test framework exists |
| done | Create or update `.env.example` | Runway placeholders added; no real secrets |
| done | Run `scripts/agent_repo_audit.py` | Generated local `AI_REPO_AUDIT.md`, ignored by git |
| done | Create public GitHub repo | Created `https://github.com/TechmanStudios/top-comment-studio` as a public repository; local `origin` is configured |

## MVP

| Status | Task | Notes |
|---|---|---|
| todo | Define MVP user flow | Keep demo-focused |
| todo | Implement smallest end-to-end path | Avoid premature abstractions |
| todo | Add smoke test or validation check | Prefer simple and fast |
| todo | Add error states | Make demo resilient |

## Demo Polish

| Status | Task | Notes |
|---|---|---|
| todo | Write demo script | See `docs/DEMO_SCRIPT.md` |
| todo | Add sample data | No secrets or private data |
| todo | Check fresh clone setup | Run from clean environment |
| todo | Document known limitations | See `KNOWN_ISSUES.md` |

## Agent Handoff Notes

Add dated notes here after major sessions.

```text
YYYY-MM-DD — Agent:
- Summary:
- Validation:
- Blockers:
- Next step:
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Inventoried the scaffold, added README, Runway resources, project inventory, and safe environment variable setup for Top Comment Studio.
- Validation: Ran `python scripts/agent_repo_audit.py`; confirmed `.env` and `AI_REPO_AUDIT.md` are ignored by git.
- Blockers: Dev/build/test commands cannot be verified until the MVP stack is chosen.
- Next step: Choose the MVP stack, then add and push the first commit to `TechmanStudios/top-comment-studio`.
```

```text
2026-05-09 — GitHub Copilot:
- Summary: Created the public GitHub repository `TechmanStudios/top-comment-studio` and verified the local `origin` remote points to it.
- Validation: `gh repo view TechmanStudios/top-comment-studio` reports visibility `PUBLIC`.
- Blockers: No repo-creation blocker remains.
- Next step: Create the initial commit and push when Bryan is ready.
```
