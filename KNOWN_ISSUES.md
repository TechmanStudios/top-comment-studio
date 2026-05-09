# Known Issues

Track setup blockers, bugs, and limitations here.

## Template

```text
Issue:
Impact:
Reproduction:
Current workaround:
Owner:
Status:
```

---

## Current Issues

### App Scaffold Not Implemented

Issue: A recommended Python/FastAPI/uv stack is documented, but no app framework, package manifest, entry point, dev command, build command, or test command has been implemented yet.
Impact: Fresh-clone run instructions are still limited to documentation review and the audit script.
Reproduction: Run `python scripts/agent_repo_audit.py` from the repo root.
Current workaround: Follow `docs/NEXT_PHASE_BUILD_PLAN.md` to add the first implementation scaffold.
Owner: Bryan / project team.
Status: open

## Resolved Issues

### GitHub Repo Creation Permission

Issue: The available GitHub CLI token cannot create `TechmanStudios/top-comment-studio`.
Impact: Resolved. The repository now exists publicly at `https://github.com/TechmanStudios/top-comment-studio`.
Reproduction: Run `gh repo create TechmanStudios/top-comment-studio --public --description 'Audience-in-the-loop YouTube Shorts workflow powered by Runway API.'`.
Current workaround: None needed.
Owner: Bryan / TechmanStudios admin.
Status: resolved
