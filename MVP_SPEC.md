# MVP Spec: AI YouTube Audience-in-the-Loop Engine

## Purpose

Build the smallest useful version of the AI YouTube project: a short-form-first content workflow where the audience helps decide the next video through comments.

The MVP should prove the creative loop before adding heavy automation.

```text
Previous Short
  -> audience comments
  -> selected safe audience signal
  -> generated next Short package
  -> Bryan reviews
  -> next Short is published
  -> loop repeats
```

## Product Thesis

The channel should not guess what the audience wants.

The channel should listen, interpret, and respond.

The MVP is successful when Bryan can take a top audience comment and quickly generate the next short-form video package while preserving safety, continuity, and creative control.

## Primary User

Bryan, as the creator/operator of the AI YouTube channel.

## Secondary Users

- AI coding agents helping build the workflow.
- AI creative agents helping generate scripts, prompts, and titles.
- Future collaborators helping produce or edit Shorts.
- The YouTube audience indirectly guiding the series.

## Core MVP Flow

1. Bryan publishes a YouTube Short.
2. Viewers comment with ideas, questions, branches, or challenges.
3. Bryan or an agent selects the strongest usable audience signal.
4. The system checks that signal against guardrails.
5. The system generates a next-video package.
6. Bryan reviews, edits, and approves.
7. The next Short is created and published.
8. The series-chain record is updated.

## MVP Input

The first version may use manual input.

Required input:

```text
Previous video title
Previous video summary
Previous video CTA
Selected audience comment
Optional comment metadata:
  - author display name
  - like count
  - reply count
  - timestamp
  - reason selected
```

Optional input:

```text
Video URL
YouTube video ID
Full list of candidate comments
Bryan's creative notes
Target tone
Target duration
Visual style
Voiceover style
```

## MVP Output

The system should generate:

```text
Short script
Voiceover text
Title options
Description
Pinned comment / CTA
Visual prompt
Video generation prompt
Thumbnail idea
Safety notes
Series-chain update
```

## Required Files or Data Records

The MVP should maintain a record of the chain.

Minimum record fields:

```json
{
  "episode_id": "episode_001",
  "title": "",
  "summary": "",
  "youtube_video_id": "",
  "source_comment": {
    "text": "",
    "author": "",
    "likes": 0,
    "selection_reason": ""
  },
  "safe_interpretation": "",
  "generated_script": "",
  "next_cta": "",
  "status": "draft"
}
```

## Short-Form First

The MVP should prioritize YouTube Shorts.

Default target:

```text
Duration: 20-45 seconds
Format: vertical video
Hook: first 1-3 seconds
Structure: fast setup, payoff, next CTA
```

The first system does not need long-form video support.

## Core Features

### 1. Comment Input

Allow Bryan or an agent to provide a selected comment manually.

This can be a form, JSON file, Markdown file, CLI prompt, or simple text input.

### 2. Guardrail Check

Evaluate whether the comment is safe, usable, and brand-aligned.

Possible statuses:

```text
approved
approved_with_redirect
needs_human_review
rejected
```

### 3. Creative Interpretation

Convert the audience comment into a usable creative seed.

Example:

```text
Raw comment:
"Make the AI build a floating city."

Creative seed:
"The next episode shows the AI responding to the audience's request by designing a floating city above a stormy ocean."
```

### 4. Short Script Generation

Generate a short-form script with:

```text
Hook
Setup
Action / reveal
Audience acknowledgment
Next CTA
```

### 5. Production Prompt Generation

Generate prompts for AI video, image, or animation tools.

The prompt should include:

```text
Scene
Style
Motion
Camera direction
Mood
Key objects
Avoid list
```

### 6. Series Chain Logging

Every generated episode should connect back to the selected audience signal.

## Non-Goals for MVP

Do not prioritize these in the first version:

```text
Full YouTube API automation
OAuth
Automatic upload
Advanced analytics dashboard
Multi-channel management
Complex database architecture
Enterprise moderation
Long-form video production
Full social scheduling
```

These may come later.

## Definition of Done

The MVP is ready when Bryan can:

- Enter or paste a top comment.
- Run the workflow.
- Receive a complete next-Short package.
- See whether the comment passed guardrails.
- Preserve the episode chain.
- Review and approve before publishing.

## Agent Guidance

Agents should not turn this into a generic content scheduler.

Every major feature should strengthen this loop:

```text
Audience signal
  -> safe interpretation
  -> creator approval
  -> next short-form video
  -> new audience signal
```
