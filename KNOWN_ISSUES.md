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

### Stack Not Selected

Issue: No app framework, package manager, entry point, dev command, build command, or test command exists yet.
Impact: Fresh-clone run instructions are limited to documentation review and the audit script.
Reproduction: Run `python scripts/agent_repo_audit.py` from the repo root.
Current workaround: Choose the MVP stack before adding implementation code.
Owner: Bryan / project team.
Status: open

### GitHub Repo Creation Permission

Issue: The available GitHub CLI token cannot create `TechmanStudios/top-comment-studio`.
Impact: Resolved. The repository now exists publicly at `https://github.com/TechmanStudios/top-comment-studio`.
Reproduction: Run `gh repo create TechmanStudios/top-comment-studio --public --description 'Audience-in-the-loop YouTube Shorts workflow powered by Runway API.'`.
Current workaround: None needed.
Owner: Bryan / TechmanStudios admin.
Status: resolved
