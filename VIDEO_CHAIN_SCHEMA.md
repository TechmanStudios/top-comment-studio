# Video Chain Schema

## Purpose

This file defines the data structure for tracking the audience-driven video chain.

The video chain is the memory spine of the AI YouTube project.

Each episode should know:

- What came before it.
- Which audience signal shaped it.
- What it produced.
- What decision it asks the audience to make next.

## Conceptual Model

```text
Episode
  -> audience response
  -> selected comment or theme
  -> safe interpretation
  -> generated next episode
  -> next audience prompt
```

## Minimal Episode Record

```json
{
  "episode_id": "episode_001",
  "series_id": "main",
  "status": "draft",
  "title": "",
  "summary": "",
  "youtube": {
    "video_id": "",
    "url": "",
    "published_at": ""
  },
  "source": {
    "previous_episode_id": null,
    "source_type": "original_prompt",
    "source_text": ""
  },
  "selected_audience_signal": {
    "selection_mode": "top_comment",
    "comment_text": "",
    "author_display_name": "",
    "like_count": 0,
    "reply_count": 0,
    "theme": "",
    "reason_selected": ""
  },
  "safety": {
    "status": "approved",
    "notes": "",
    "safe_interpretation": ""
  },
  "production": {
    "script": "",
    "voiceover": "",
    "visual_prompt": "",
    "video_prompt": "",
    "title_options": [],
    "description": "",
    "tags": [],
    "thumbnail_idea": ""
  },
  "next_audience_prompt": "",
  "created_at": "",
  "updated_at": ""
}
```

## Episode Status Values

Use these statuses:

```text
idea
draft
needs_review
approved
produced
published
archived
rejected
```

## Safety Status Values

Use these values:

```text
approved
approved_with_redirect
needs_human_review
rejected
```

## Selection Mode Values

Use these values:

```text
original_prompt
top_comment
top_theme
creator_pick
redirected_comment
combined_comments
manual_seed
```

## Recommended Folder Structure

```text
chains/
  main/
    episode_001.json
    episode_002.json
    episode_003.json

scripts/
  episode_001.md
  episode_002.md

comments/
  episode_001_comments.json
  episode_002_comments.json

outputs/
  episode_001/
    script.md
    prompts.md
    metadata.json
```

## Series Manifest

Each series may have a manifest.

```json
{
  "series_id": "main",
  "series_title": "Audience Builds an AI World",
  "description": "",
  "tone": "curious, cinematic, playful",
  "default_duration_seconds": 35,
  "episodes": [
    "episode_001",
    "episode_002"
  ],
  "active": true
}
```

## Comment Record

If raw or candidate comments are stored, use this structure:

```json
{
  "comment_id": "",
  "video_id": "",
  "author_display_name": "",
  "text": "",
  "like_count": 0,
  "reply_count": 0,
  "published_at": "",
  "updated_at": "",
  "is_candidate": true,
  "safety_status": "approved",
  "notes": ""
}
```

## Generated Short Package

A generated short package should include:

```json
{
  "episode_id": "episode_002",
  "hook": "",
  "script": "",
  "voiceover": "",
  "visual_prompt": "",
  "video_prompt": "",
  "caption_text": "",
  "title_options": [],
  "description": "",
  "pinned_comment": "",
  "next_cta": "",
  "safety_notes": ""
}
```

## Chain Integrity Rules

1. Every generated episode should reference its previous episode unless it begins a new series.
2. Every audience-driven episode should store the selected audience signal.
3. Every selected signal should have a safety status.
4. Every safe redirect should preserve the original comment and the rewritten interpretation.
5. Every episode should include a next audience prompt unless the series is ending.

## Agent Guidance

Agents should use this schema as a starting point, not a prison.

If the implementation stack needs a database model, TypeScript type, Python dataclass, Pydantic model, JSON schema, or Markdown record, preserve these concepts:

```text
episode
audience signal
safety status
creative interpretation
production package
next prompt
chain continuity
```
