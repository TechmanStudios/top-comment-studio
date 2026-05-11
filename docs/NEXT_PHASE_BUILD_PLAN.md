# Next Phase Build Plan

Use this as the handoff from project setup into implementation.

## Goal

Build the smallest runnable Top Comment Studio vertical slice:

```text
selected audience comment
  -> guardrail review
  -> safe creative interpretation
  -> Shorts production package
  -> series-chain record
  -> optional Runway workflow prompt/endpoint handoff
```

## Recommended Stack

- Runtime: Python 3.12+
- Package manager: `uv`
- Web framework: FastAPI
- UI: server-rendered Jinja templates with vanilla CSS/JavaScript for the first demo
- Storage: local JSON files under `data/` for the MVP; move to SQLite only if JSON becomes painful
- Validation: pytest plus one smoke test for the comment-to-package flow
- Runway integration: server-side client only; use `.env` for `RUNWAYML_API_SECRET`

## Why This Stack

This keeps the first implementation Python-first, simple to run, easy for agents to modify, and compatible with a local demo. It avoids a heavier frontend build until the core workflow exists.

## First Implementation Slice

1. Done: add `pyproject.toml` with FastAPI, Uvicorn, Pydantic, python-dotenv, httpx, Jinja2, and pytest.
2. Done: add `src/top_comment_studio/` with app entrypoint, schemas, guardrail rules, package generator, and JSON chain storage.
3. Done: add a single page and route for manual comment input.
4. Done: generate a deterministic draft package first, with optional LLM/Runway calls deferred behind explicit later buttons.
5. Done: save generated episodes under ignored local JSON storage.
6. Done: add a smoke test that verifies a sample comment produces a safe package and chain record.
7. Done: update README with real install/dev/test commands.

## Current Workflow Model Stack

- Text generation in workflows: GPT 5.5
- Image generation in workflows/direct API: Nano Banana Pro / Gemini 3 Pro Image (`gemini_image3_pro` in the API)
- Fast image fallback: Nano Banana / Gemini 2.5 Flash (`gemini_2.5_flash` in the API)
- Video generation in workflows: Seedance 2.0

## Initial Commands To Add

```powershell
uv sync
uv run uvicorn top_comment_studio.app:app --reload
uv run pytest
```

## Runway Workflow Design Target

The first custom Runway workflow should be shaped around these inputs:

```json
{
  "episode_id": "episode_002",
  "safe_interpretation": "",
  "visual_style": "vertical cinematic YouTube Short",
  "shot_list": [],
  "video_prompt": "",
  "duration_seconds": 10,
  "aspect_ratio": "720:1280"
}
```

Expected outputs:

```json
{
  "workflow_task_id": "",
  "status": "",
  "asset_urls": [],
  "notes": ""
}
```

Custom workflow endpoints should be recorded from:

https://dev.runwayml.com/organization/8f8366b8-b7b6-4f9c-baae-f72c16c9f79f/workflows

## Keep Out Of Scope Until The Slice Works

- YouTube OAuth
- Automatic publishing
- Multi-user accounts
- Advanced analytics
- Full video editing timeline
- Background polling loops without user action
