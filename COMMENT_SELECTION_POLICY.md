# Comment Selection Policy

## Purpose

This document defines how the project chooses audience comments to guide the next video in the AI YouTube series.

The goal is to keep the channel audience-directed while preserving safety, quality, continuity, and Bryan's creative control.

## Core Principle

The audience leads the direction.

Bryan remains the final creative director.

The system should honor the strongest audience signal whenever it is safe, feasible, and aligned with the channel.

## Default Selection Rule

The default rule is:

```text
The top usable comment becomes the seed for the next video.
```

“Top” usually means the highest-liked comment, but the system should also consider replies, repeated themes, and quality.

## What Counts as a Usable Comment?

A usable comment is one that:

- Is safe for YouTube.
- Fits the channel concept.
- Can become a short-form video.
- Connects to the current series chain.
- Is not spam.
- Is not harassment.
- Is not a request for harmful or deceptive content.
- Gives the next video a clear creative direction.

## Comment Ranking Signals

Use these signals when selecting a comment:

1. Like count.
2. Reply count.
3. Repeated themes across multiple comments.
4. Creativity.
5. Clarity.
6. Fit with the current video chain.
7. Feasibility for short-form production.
8. Safety and platform fit.

The highest-liked comment is important, but it is not the only signal.

## Selection Modes

### Mode 1: Top Comment

Use the single highest-liked safe comment.

Best for simple audience-driven episodes.

### Mode 2: Top Theme

Use a repeated idea across many comments.

Best when many viewers ask for the same thing in different words.

### Mode 3: Creator Pick from Top Comments

Bryan chooses from the top safe comments.

Best when several comments are strong.

### Mode 4: Redirected Top Comment

Use the spirit of the top comment, but rewrite it into a safe and brand-aligned version.

Best when the top comment has a good creative spark but unsafe wording or details.

## Unsafe or Unusable Top Comments

If the top comment is unsafe, spammy, abusive, off-brand, impossible, or low-quality, do not use it directly.

Instead:

1. Preserve the underlying safe creative intent if possible.
2. Redirect it into a safe version.
3. If no safe version exists, skip to the next strongest usable comment.
4. Document the reason.

Example:

```text
Original comment:
"Make the AI destroy a real city."

Safe interpretation:
"The AI runs a fictional city simulation where a design failure causes a dramatic collapse scenario."

Status:
approved_with_redirect
```

## Spam Handling

A comment should be considered spam if it is:

- Repeated copy-paste text.
- Promotional with no creative relevance.
- Bot-like.
- A scam.
- Mostly links.
- Unrelated to the video.
- Manipulating engagement without contributing an idea.

Spam should never become the next video seed.

## Offensive or Harassing Comments

Do not select comments that target real people or groups with abuse, dehumanization, harassment, or hateful framing.

If there is a safe fictional or educational version, use a redirect. Otherwise reject.

## Creator Override

Bryan may override the selected comment.

Valid reasons include:

- Safety.
- Brand fit.
- Better continuity.
- Production feasibility.
- Legal/copyright concerns.
- Stronger creative direction.
- Avoiding repetitive episodes.
- Protecting the community.

When overriding, the system should still respect the audience signal where possible.

## Combining Comments

If several comments point to the same idea, the system may combine them into one creative seed.

Example:

```text
Comment A:
"Build a floating city."

Comment B:
"Make it powered by storms."

Comment C:
"What if the city flies over the ocean?"

Combined seed:
"The community wants a floating storm-powered ocean city."
```

## Tie-Breaking

When comments are equally strong, prefer the one that:

1. Best continues the current chain.
2. Creates the clearest short-form hook.
3. Is safest.
4. Is easiest to produce.
5. Opens the best next audience decision.

## Selection Record

Each selected comment should produce a record:

```json
{
  "selected_comment_text": "",
  "author_display_name": "",
  "likes": 0,
  "selection_mode": "top_comment",
  "safety_status": "approved",
  "safe_interpretation": "",
  "reason_selected": "",
  "reason_modified_or_skipped": ""
}
```

## Audience Transparency

When useful, the next video should acknowledge the audience's role.

Examples:

```text
"Top comment said to build a floating city, so here we go."

"The community chose the storm-powered version."

"Y'all voted for chaos. The AI listened."
```

Do not over-explain moderation decisions in the video unless it helps the audience understand the redirect.

## Policy Summary

The audience gets the wheel.

Bryan keeps the brakes.

The system helps turn the strongest safe audience signal into the next video.
