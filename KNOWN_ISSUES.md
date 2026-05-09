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

### Runway Workflow Submit Not Implemented

Issue: The app generates local draft packages, but does not submit jobs to Runway yet.
Impact: The demo can show comment-to-package generation, but media generation still requires manual Runway workflow execution.
Reproduction: Generate a package from the web form and inspect the workflow model stack output.
Current workaround: Copy the generated prompts into the Runway app workflow manually until the endpoint integration is implemented.
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
