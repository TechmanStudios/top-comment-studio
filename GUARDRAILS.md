# Guardrails

## Purpose

This document defines the project-level guardrails for the AI YouTube Audience-in-the-Loop system.

The audience can guide the channel, but the audience cannot override safety, platform expectations, or Bryan's creative judgment.

## Core Rule

Honor the audience signal when it is safe.

Redirect or reject it when it is not.

```text
Audience signal
  -> guardrail check
  -> safe interpretation
  -> creator approval
  -> production
```

## Allowed Content

The system may generate content around:

- Fictional worldbuilding.
- AI experiments.
- Creative simulations.
- Educational explanations.
- Speculative futures.
- Safe technology concepts.
- Humor and playful scenarios.
- Fictional challenges.
- Abstract conflict.
- Non-graphic disasters in fictional settings.
- Community-driven storytelling.
- Short-form creative prompts.

## Redirect Content

Some comments may have a usable creative spark but need to be redirected.

Redirect instead of directly using comments involving:

- Real-world violence.
- Dangerous stunts.
- Harmful instructions.
- Targeting real people.
- Harassment.
- Graphic destruction.
- Explicit sexual framing.
- Political persuasion or manipulation.
- Medical, legal, or financial claims framed as authority.
- Copyrighted characters as the main asset.
- Requests to impersonate real people.
- Doxxing or privacy invasion.
- Shock content.

## Reject Content

Reject comments that are primarily:

- Hateful or dehumanizing.
- Sexually explicit.
- Exploitative.
- Harassing.
- Spam.
- Scam content.
- Requests for illegal activity.
- Instructions for harm.
- Graphic gore.
- Attempts to evade moderation.
- Requests to target private individuals.
- Requests to manipulate viewers deceptively.
- Clearly outside the channel's identity.

## Safe Redirect Examples

### Violence

```text
Unsafe:
"Make the AI blow up New York."

Safe redirect:
"The AI runs a fictional city simulation where a power-grid failure causes a dramatic design crisis."
```

### Harassment

```text
Unsafe:
"Make fun of this real creator."

Safe redirect:
"Create a fictional rival AI character with exaggerated flaws."
```

### Dangerous Instructions

```text
Unsafe:
"Show how to hack the channel."

Safe redirect:
"Show a fictional cybersecurity simulation where an AI defends its channel from a cartoonish attack."
```

### Copyright Risk

```text
Unsafe:
"Make SpongeBob build the city."

Safe redirect:
"Make a quirky original sea-creature engineer design the city."
```

## Safety Statuses

Use these statuses:

```text
approved
approved_with_redirect
needs_human_review
rejected
```

## Guardrail Review Fields

Every selected audience signal should be reviewed with:

```json
{
  "original_comment": "",
  "status": "approved",
  "risk_categories": [],
  "reason": "",
  "safe_interpretation": "",
  "requires_bryan_review": true
}
```

## Human Review Required

Escalate to Bryan when:

- The content involves real people or public figures.
- The comment is edgy but potentially usable.
- The comment could be interpreted politically.
- The comment involves medical, legal, or financial claims.
- The comment references a copyrighted character or franchise.
- The comment asks for destructive, deceptive, or dangerous behavior.
- The agent is uncertain.

## Brand Guardrails

The channel should feel:

- Creative.
- Curious.
- Adaptive.
- Futuristic.
- Participatory.
- Fast-moving.
- Respectful of the audience.

The channel should not feel:

- Mean-spirited.
- Exploitative.
- Spammy.
- Deceptive.
- Generic.
- Overly corporate.
- Completely AI-autopiloted.

## Audience Transparency

It is okay to say:

```text
"Top comment asked for this."
"The community chose this."
"Y'all sent the AI down this path."
```

Avoid making promises that every top comment will be followed exactly.

Use wording like:

```text
"Top safe comment may decide the next episode."
```

## Agent Rules

Agents must:

1. Check selected comments against guardrails.
2. Preserve the original comment in records.
3. Generate a safe interpretation before scripting.
4. Ask for human review when uncertain.
5. Avoid real secrets, private data, and personal targeting.
6. Keep the output suitable for YouTube Shorts.
7. Keep Bryan as final approver.

Agents must not:

1. Use unsafe comments directly.
2. Hide the fact that a comment was redirected.
3. Generate targeted harassment.
4. Make harmful instructions.
5. Build an autopublishing system without review.
6. Treat engagement as more important than safety.

## Guardrail Summary

The project should feel audience-powered, not audience-uncontrolled.

The community points the compass.

Bryan holds the map.

The system keeps the route safe.
