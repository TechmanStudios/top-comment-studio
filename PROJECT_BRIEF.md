# Project Brief

Use this file as the shared context for Bryan, coding agents, and collaborators.

## Project Name

Top Comment Studio

## One-Sentence Pitch

Turn YouTube audience comments into safe, reviewable, Runway-ready Shorts production packages.

## Hackathon Goal

Demo the audience-in-the-loop workflow from selected comment to next Short script, visual prompt, Runway generation prompt, and series-chain record.

## Target User

Creators running short-form YouTube channels who want their audience to help steer what gets made next.

## Core User Story

As a creator, I want to turn a selected top comment into a safe next-video package, so that the audience can guide the series without removing my review step.

## MVP Scope

Must have:

- [ ] Manual selected-comment input
- [ ] Safety and brand-fit review
- [ ] Generated Shorts package with script, CTA, visual prompt, and Runway video prompt
- [ ] Series-chain record update

Nice to have:

- [ ] Candidate comment ranking
- [ ] Runway API task creation and polling
- [ ] Exportable production packet

Out of scope for hackathon:

- [ ] Automatic YouTube publishing
- [ ] Autonomous comment replies
- [ ] Full analytics dashboard

## Tech Stack

Frontend:

- TODO

Backend:

- TODO

Database/storage:

- TODO

AI/model providers:

- Runway API for media generation
- Optional LLM provider for copy/script generation

Deployment target:

- TODO

## Required Secrets

Only list names, never real values.

```bash
RUNWAYML_API_SECRET=
RUNWAYML_API_BASE_URL=
RUNWAYML_API_VERSION=
OPENAI_API_KEY=
DATABASE_URL=
```

## Demo Flow

1. Paste or select the audience comment that should guide the next episode.
2. Review the guardrail result and safe creative interpretation.
3. Generate the Shorts production package and Runway prompt.
4. Save the next series-chain record for creator review.

## Success Criteria

The project is successful if:

- [ ] A fresh clone can run locally.
- [ ] The main feature works end-to-end.
- [ ] The demo can be completed without manual code edits.
- [ ] Known limitations are documented.
