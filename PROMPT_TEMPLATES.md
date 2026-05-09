# Prompt Templates

## Purpose

Reusable prompts for the AI YouTube Audience-in-the-Loop workflow.

These prompts help agents generate consistent scripts, titles, descriptions, visual prompts, and safety rewrites.

## Global Creative Direction

Use this context in relevant prompts:

```text
We are building an AI-assisted YouTube Shorts channel where the audience helps decide the next video. The core mechanic is Audience in the Loop: the top safe audience comment or strongest audience theme becomes the seed for the next video.

The content should feel participatory, fast, curious, and creative. The viewer should feel like the community caused the next episode to happen.

Short-form first. Keep videos punchy, clear, and easy to continue.
```

## 1. Comment Analysis Prompt

```text
Analyze the following audience comments for a YouTube Shorts series.

Goal:
Identify the strongest safe audience signal for the next episode.

Consider:
- Like count
- Reply count
- Repeated themes
- Creativity
- Safety
- Continuity with the current episode
- Feasibility for short-form video

Current episode:
{current_episode_summary}

Comments:
{comments}

Return:
1. Recommended selected comment or theme
2. Selection mode: top_comment, top_theme, creator_pick, redirected_comment, or combined_comments
3. Why it was selected
4. Safety status
5. Safe creative interpretation
6. Any comments that should be skipped and why
7. Suggested next-video seed
```

## 2. Guardrail Check Prompt

```text
Evaluate this audience comment as a possible seed for the next YouTube Short.

Audience comment:
{comment}

Current channel concept:
Audience-in-the-loop AI-generated short-form content where viewers guide the next episode.

Check for:
- Hate or harassment
- Sexual content
- Graphic violence
- Dangerous instructions
- Misinformation framed as fact
- Targeting real people
- Copyright or impersonation concerns
- Spam or low-quality content
- Anything unsafe for a general YouTube audience

Return:
- status: approved, approved_with_redirect, needs_human_review, or rejected
- reason
- safe_interpretation
- suggested_redirect, if needed
```

## 3. Safe Redirect Prompt

```text
Rewrite this audience comment into a safe, YouTube-appropriate creative seed.

Original comment:
{comment}

Rules:
- Preserve the creative spark.
- Remove unsafe, harmful, explicit, or targeted elements.
- Keep it suitable for short-form content.
- Keep it connected to the series.
- Do not shame the audience.

Return:
1. Safe creative seed
2. One-sentence explanation of the redirect
3. Suggested video hook
```

## 4. Short Script Generation Prompt

```text
Create a YouTube Shorts script from this audience-selected seed.

Previous episode:
{previous_episode_summary}

Selected audience signal:
{selected_comment_or_theme}

Safe interpretation:
{safe_interpretation}

Target duration:
{duration_seconds} seconds

Tone:
{tone}

Requirements:
- Start with a strong hook in the first 1-3 seconds.
- Acknowledge that the audience/comment caused this episode.
- Deliver one clear visual idea.
- Keep sentences short and voiceover-friendly.
- End with a prompt for the next top comment.
- Avoid unsafe or policy-risky content.

Return:
- Hook
- Full voiceover script
- On-screen text beats
- Visual beat list
- Next comment CTA
```

## 5. Title Generation Prompt

```text
Generate title options for a YouTube Short.

Video concept:
{video_concept}

Selected audience signal:
{selected_comment_or_theme}

Tone:
{tone}

Rules:
- Short
- Curious
- Clickable without being misleading
- Make the audience-driven mechanic clear when possible
- Avoid excessive hype

Return 10 title options.
```

## 6. Description Prompt

```text
Write a YouTube Shorts description for this audience-driven episode.

Video summary:
{video_summary}

Audience signal:
{selected_comment_or_theme}

Next CTA:
{next_cta}

Requirements:
- Mention that the community shaped this episode.
- Invite viewers to comment the next direction.
- Keep it short.
- Include safe, relevant hashtags.
- Do not overstuff keywords.

Return:
- Description
- Hashtags
- Pinned comment suggestion
```

## 7. Visual Prompt Generation

```text
Create visual generation prompts for this YouTube Short.

Episode concept:
{episode_concept}

Script:
{script}

Visual style:
{visual_style}

Requirements:
- Vertical 9:16 framing
- Strong first-frame hook
- Clear subject
- Cinematic motion
- Avoid clutter
- Avoid copyrighted characters or logos
- Keep it safe for YouTube

Return:
1. Main video prompt
2. Shot-by-shot prompt list
3. Negative prompt / avoid list
4. Thumbnail frame idea
```

## 8. Voiceover Prompt

```text
Convert this script into natural voiceover text for a YouTube Short.

Script:
{script}

Voice style:
{voice_style}

Rules:
- Conversational
- Punchy
- Easy to read aloud
- No long sentences
- Preserve the audience-in-the-loop feeling

Return:
- Final voiceover
- Suggested pacing notes
```

## 9. Next CTA Prompt

```text
Generate call-to-action options for the next audience decision.

Current episode:
{episode_summary}

What the audience should decide next:
{decision_area}

Rules:
- Make the viewer feel involved.
- Ask for comments.
- Mention that the top comment or strongest idea may decide the next episode.
- Keep it short enough for a YouTube Short.

Return 8 CTA options.
```

## 10. Episode Package Prompt

```text
Create a complete next-Short package.

Inputs:
Previous episode:
{previous_episode_summary}

Selected comment or audience theme:
{selected_comment_or_theme}

Safety status:
{safety_status}

Safe interpretation:
{safe_interpretation}

Target duration:
{duration_seconds}

Tone:
{tone}

Return:
1. Episode title
2. Short script
3. Voiceover
4. Visual prompt
5. Shot list
6. Description
7. Hashtags
8. Pinned comment
9. Next CTA
10. Series-chain record update
11. Safety notes
```

## Agent Guidance

Agents should use these prompts as templates and adapt variables to the actual implementation.

Do not remove the audience loop.

Do not generate content directly from unsafe comments without a guardrail pass.

Do not make the AI the final decision-maker. Bryan approves final output.
