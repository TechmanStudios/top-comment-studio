# Top Comment Studio — Project Timeline & Agent Guide

_Last updated: 2026-05-09_

## Project Name

**Top Comment Studio**

## North Star

Top Comment Studio turns high-signal audience comments into AI-generated short-form video production packages.

Core phrase:

> **Audience-in-the-loop media generation**

The product is not just an AI video generator. It is a creator workflow where audience feedback becomes the creative input, AI agents become the production team, and Runway becomes the visual media engine.

---

## Official Hackathon Context

Runway API Hackathon, May 8–11, 2026.

Current status as of 2026-05-09:

- Registration is closed.
- Submissions are open.
- Submission deadline: **Monday, May 11, 2026 at 9:00 AM ET**.
- Submission requires a short project description and demo video.
- Live project link is optional, but strongly preferred if available.
- Project must run on the **Runway API**.
- The challenge is to build an **agent, app, tool, or creative workflow** that creates, manipulates, or orchestrates media.
- Judging criteria:
  - Creativity
  - Technical depth
  - Impact
  - Polish

Primary official references:

- https://runwayml.com/api-hackathon
- https://runwayml.com/api-hackathon-terms

---

## Product Thesis

Most AI video tools start with a blank prompt.

Top Comment Studio starts with audience signal.

Instead of:

```text
creator prompt -> AI video
```

Top Comment Studio does:

```text
audience comment -> signal analysis -> creative direction -> Runway media generation -> Shorts package
```

This makes the creator's audience part of the creative loop without removing the creator's control.

---

## MVP Definition

The hackathon MVP should prove this loop:

```text
comment input
  -> audience insight
  -> Director brief
  -> script
  -> shot list
  -> Runway prompts
  -> generated media preview
  -> creator-ready output package
```

### Required MVP Features

1. Comment input
   - Manual pasted comment is acceptable for MVP.
   - YouTube URL ingestion is a stretch goal.

2. Audience Signal Analysis
   - Viewer intent
   - Emotional driver
   - Content opportunity
   - Visual potential
   - Shorts suitability score

3. Director Agent Output
   - Title
   - Hook
   - 30–45 second script
   - Beat map
   - Shot list
   - CTA

4. Runway Prompt Builder
   - Scene prompts
   - Camera direction
   - Visual style
   - Reference/style notes

5. Runway Media Generation
   - At least one generated image or video asset.
   - Ideally 3–5 generated visual assets.

6. Output Package
   - Generated assets
   - Script
   - Captions
   - Title
   - Description
   - Hashtags
   - Thumbnail concept

### Stretch Features

Only build these after the MVP works end-to-end:

- YouTube comment fetching
- Multiple comment ranking
- Full video stitching
- Voiceover generation
- Thumbnail image generation
- Channel style memory
- Export as ZIP
- Project save/load
- Multiple creator profiles

---

## Scope Guardrails for Agents

Agents must protect the MVP.

Do not expand the project into:

- A full YouTube publishing platform
- A social media scheduler
- A full video editor
- A multi-user SaaS dashboard
- A payment platform
- A complex autonomous channel manager
- A giant plugin ecosystem

The goal is a polished, working demo.

If a feature does not support the core loop, defer it.

Core loop:

```text
audience comment -> AI creative direction -> Runway media -> creator-ready Shorts package
```

---

## Recommended Repo Structure

```text
top-comment-studio/
  README.md
  PROJECT_TIMELINE.md
  .env.example
  pyproject.toml

  src/
    top_comment_studio/
      app.py
      settings.py
      schemas.py
      guardrails.py
      package_generator.py
      storage.py

      runway/
        client.py
        workflows.py
        prompts.py

      templates/
        index.html
        package.html

      static/
        app.css
        app.js

  data/
    samples/
      sample_comments.json
      sample_packages.json

  tests/
    test_smoke_comment_to_package.py
```

---

## Agent Roles

### 1. Project Manager Agent

Purpose:

Keep the build aligned with the hackathon deadline and MVP.

Responsibilities:

- Maintain the project timeline.
- Identify blockers.
- Prevent scope creep.
- Keep tasks small and shippable.
- Make sure every task supports the demo.

Default behavior:

- Prefer a working simple version over a clever incomplete version.
- Ask: "Does this help the Monday 9 AM demo?"

---

### 2. Comment Scout Agent

Purpose:

Analyze audience comments and extract creative signal.

Input:

```json
{
  "comment": "Can you make a video showing how AI turns one creator into a whole studio?"
}
```

Output:

```json
{
  "viewer_intent": "The viewer wants a relatable explainer about AI-augmented creativity.",
  "emotional_driver": "Empowerment, curiosity, creative possibility.",
  "content_opportunity": "Show a solo creator becoming a full production team through AI tools.",
  "shorts_suitability_score": 0.92
}
```

---

### 3. Creative Strategist Agent

Purpose:

Decide how to turn the audience signal into a strong short-form concept.

Responsibilities:

- Identify the best angle.
- Decide the tone.
- Create a viewer promise.
- Make sure the idea has visual potential.

Output should include:

- Core angle
- Audience payoff
- Viral hook
- Risk notes
- Visual opportunity

---

### 4. Director Agent

Purpose:

Turn the selected comment into a production-ready Short.

Responsibilities:

- Write title.
- Write hook.
- Write script.
- Create beat map.
- Define pacing.
- Define CTA.

Output should be structured JSON when possible.

Preferred output shape:

```json
{
  "title": "",
  "hook": "",
  "duration_seconds": 40,
  "script": "",
  "beats": [
    {
      "beat_number": 1,
      "timestamp": "0:00-0:05",
      "narration": "",
      "visual_goal": ""
    }
  ],
  "cta": ""
}
```

---

### 5. Cinematographer Agent

Purpose:

Convert the Director brief into Runway-ready prompts.

Responsibilities:

- Create visual prompts.
- Add camera direction.
- Add lighting direction.
- Add motion style.
- Maintain visual continuity.
- Avoid prompt bloat.

Preferred output shape:

```json
{
  "shots": [
    {
      "shot_number": 1,
      "duration_seconds": 5,
      "runway_prompt": "",
      "camera_motion": "",
      "lighting": "",
      "style_notes": "",
      "negative_prompt_notes": ""
    }
  ]
}
```

---

### 6. Runway Integration Agent

Purpose:

Wire the app to the Runway API.

Responsibilities:

- Keep API key handling secure.
- Implement generation functions.
- Return usable asset URLs or local file references.
- Fail gracefully when a generation fails.
- Log request IDs when available.

Required functions, even if initially stubbed:

```python
generate_image(prompt: str, aspect_ratio: str = "9:16") -> dict
generate_video(prompt: str, duration_seconds: int = 5, aspect_ratio: str = "9:16") -> dict
check_generation_status(task_id: str) -> dict
```

---

### 7. Editor Agent

Purpose:

Package the creative output for a creator.

Responsibilities:

- Create caption text.
- Create upload title.
- Create description.
- Create hashtags.
- Create thumbnail concept.
- Create final timeline notes.

The Editor does not need to perform full video stitching for MVP unless time allows.

---

## Data Contracts

### Comment Analysis Contract

```json
{
  "comment": "",
  "viewer_intent": "",
  "emotional_driver": "",
  "content_opportunity": "",
  "visual_potential": "",
  "shorts_suitability_score": 0.0
}
```

### Director Brief Contract

```json
{
  "project_name": "Top Comment Studio",
  "source_comment": "",
  "audience_signal": {},
  "title": "",
  "hook": "",
  "script": "",
  "duration_seconds": 40,
  "beats": [],
  "shots": [],
  "thumbnail": {},
  "upload_copy": {}
}
```

### Shot Contract

```json
{
  "shot_number": 1,
  "duration_seconds": 5,
  "visual_description": "",
  "runway_prompt": "",
  "camera_motion": "",
  "style_notes": "",
  "asset_url": null,
  "status": "planned"
}
```

---

## Timeline

All times are Eastern Time.

### Saturday, May 9 — Build the spine

Goal:

Create the app skeleton and prove the text-to-brief pipeline.

Tasks:

- Create repo.
- Add `README.md`.
- Add this `PROJECT_TIMELINE.md`.
- Add `.env.example`.
- Scaffold frontend.
- Scaffold FastAPI backend.
- Create sample comment data.
- Create Director prompt/instructions file.
- Implement local-only pipeline:
  - comment input
  - audience analysis
  - Director brief
  - Runway prompt generation
- Display results in the UI.

Definition of done:

- A user can paste a comment and get a structured production brief on screen.

---

### Saturday Night, May 9 — Make it feel real

Goal:

Make the UI demoable even before media generation is complete.

Tasks:

- Add a clean landing page.
- Add "Use sample comment" button.
- Add progress stages:
  - Analyze comment
  - Direct short
  - Generate prompts
  - Generate media
  - Package output
- Add sample output cards.
- Add JSON preview or export panel.
- Add error states.

Definition of done:

- The app feels like a real product flow, even if Runway calls are still stubbed.

---

### Sunday Morning, May 10 — Wire the AI agents

Goal:

Make the Director Agent API-native.

Tasks:

- Implement OpenAI API call for Comment Scout.
- Implement OpenAI API call for Director.
- Add structured JSON outputs.
- Validate JSON responses.
- Add fallback if JSON parsing fails.
- Store sample outputs for repeatable demos.

Definition of done:

- The app produces reliable structured creative briefs from arbitrary comments.

---

### Sunday Afternoon, May 10 — Wire Runway

Goal:

Generate at least one real media asset using Runway API.

Tasks:

- Add Runway SDK/client.
- Add secure API key loading.
- Implement image generation or video generation.
- Connect generated asset to a shot card.
- Save task response.
- Show loading state.
- Show final asset preview.

Definition of done:

- A user can paste a comment and receive at least one Runway-generated visual asset tied to the Director brief.

---

### Sunday Evening, May 10 — Package the creator output

Goal:

Turn the result into a complete creator package.

Tasks:

- Add final output screen.
- Add script block.
- Add captions block.
- Add title/description/hashtags.
- Add thumbnail concept.
- Add shot list.
- Add generated media gallery.
- Add copy buttons.
- Add export JSON button if easy.

Definition of done:

- The output is useful to a real creator, even without full automated video editing.

---

### Sunday Night, May 10 — Polish and record

Goal:

Prepare submission materials.

Tasks:

- Clean UI.
- Add README screenshots or demo notes.
- Add demo script.
- Record demo video.
- Confirm public deployment.
- Confirm app does not expose API keys.
- Confirm all generated content is appropriate for general public.

Definition of done:

- Demo video is recorded.
- Live link works or repo/demo video fully explains the app.

---

### Monday Morning, May 11 — Submit before 9 AM ET

Goal:

Submit safely before the deadline.

Tasks:

- Final smoke test.
- Submit short description.
- Submit demo video.
- Submit live project link if available.
- Save confirmation.

Do not submit at the last minute.

---

## Suggested Submission Description

Top Comment Studio transforms YouTube audience comments into AI-generated Shorts production packages. It analyzes a viewer comment, extracts the creative signal, generates a Director brief, writes a script and shot list, creates Runway-ready prompts, and uses the Runway API to generate visual assets. The result is an audience-in-the-loop media workflow where comments help direct the next video while the creator stays in control.

---

## Demo Script

1. Open Top Comment Studio.
2. Paste sample comment:

```text
Can you make a video showing how AI turns one creator into a whole studio?
```

3. Click **Generate Short Package**.
4. Show audience signal analysis.
5. Show Director brief.
6. Show Runway prompts.
7. Generate visual asset.
8. Show final creator package.
9. Close with:

```text
Top Comment Studio turns audience feedback into AI-directed media production.
```

---

## Sample Comments

```json
[
  {
    "channel_type": "AI education",
    "comment": "Can you make a video showing how AI turns one creator into a whole studio?"
  },
  {
    "channel_type": "gaming",
    "comment": "Can you explain this like it's a boss fight strategy?"
  },
  {
    "channel_type": "spiritual/philosophical",
    "comment": "Can you make a short about how technology can still have soul?"
  },
  {
    "channel_type": "creator economy",
    "comment": "How would a solo creator actually use all these AI tools without getting overwhelmed?"
  }
]
```

---

## Technical Decisions

### Frontend

Recommended:

- Next.js
- Tailwind
- shadcn/ui

### Backend

Recommended:

- Python
- FastAPI
- Pydantic schemas
- Simple async job handling

### AI Layer

Recommended:

- OpenAI API for agent reasoning
- API-native Director Agent
- Do not depend on ChatGPT custom GPTs for the public app runtime

### Media Layer

Recommended:

- Runway API
- Start with image generation if video generation takes too long
- Add video generation as soon as basic image generation works

### Storage

Recommended for MVP:

- Local JSON files or SQLite

Stretch:

- Supabase

---

## Environment Variables

Create `.env.example`:

```bash
OPENAI_API_KEY=
RUNWAY_API_KEY=
APP_ENV=development
PUBLIC_APP_URL=http://localhost:3000
API_BASE_URL=http://localhost:8000
```

Never commit real API keys.

---

## Agent Coding Rules

Agents working on this repo should follow these rules:

1. Keep changes small and testable.
2. Prefer simple working code over complex abstractions.
3. Do not introduce new frameworks unless they solve an immediate MVP problem.
4. Keep API keys in environment variables only.
5. Use structured outputs for agent responses.
6. Preserve the core concept: audience-in-the-loop media generation.
7. Avoid overbuilding YouTube integrations before the comment-to-brief-to-Runway loop works.
8. Build UI states that make the demo feel end-to-end.
9. If Runway generation fails, show the planned prompt and let the demo continue.
10. Every major feature should support the Monday 9 AM submission.

---

## Current Priority Stack

Priority 1:

- Working comment input
- Working Director brief
- Working Runway prompt generation
- Working output UI

Priority 2:

- One real Runway-generated asset
- Polished demo flow
- Demo video

Priority 3:

- Full media gallery
- Export JSON
- Public deployment

Priority 4:

- YouTube API integration
- Full video stitching
- Voiceover
- Channel memory

---

## Final Definition of Done

The project is ready to submit when:

- A judge can understand the idea in 10 seconds.
- A judge can run or watch the full demo in under 3 minutes.
- The workflow clearly uses Runway API.
- The app produces a real creative output.
- The result feels useful to a real creator.
- The submission includes demo video and project description.
- The project does not leak secrets or use unsafe content.
