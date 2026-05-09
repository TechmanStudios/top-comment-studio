# YouTube API Notes

## Purpose

This file captures future automation notes for YouTube integration.

The MVP should not depend on full API automation. Start manual, prove the creative loop, then automate comment retrieval and publishing later.

## MVP Recommendation

Start with manual comment input:

```text
Bryan copies top comments
  -> system analyzes/selects
  -> system generates next Short package
  -> Bryan reviews
  -> Bryan publishes manually
```

This avoids early OAuth complexity and keeps the first version focused on the creative workflow.

## Future Automation Goals

Potential future features:

- Fetch comments from a YouTube video.
- Sort comments by like count.
- Detect repeated themes.
- Store candidate comments.
- Select the top safe comment.
- Generate next Short package.
- Track series-chain metadata.
- Draft descriptions and pinned comments.
- Eventually assist with uploads or scheduling, if desired.

## Possible API Resources

Likely YouTube Data API areas:

```text
commentThreads.list
comments.list
videos.list
playlistItems.list
search.list
```

For writing or modifying data later:

```text
commentThreads.insert
comments.insert
comments.update
comments.delete
videos.insert
thumbnails.set
```

## Comment Retrieval Concept

A later system may use:

```text
video_id
  -> commentThreads.list
  -> top-level comments
  -> sort or rank comments
  -> guardrail check
  -> selected audience signal
```

## Data to Capture from Comments

Useful fields:

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
  "parent_id": "",
  "selection_score": 0,
  "safety_status": ""
}
```

## OAuth Considerations

Reading public comments may be simpler than writing, uploading, or moderating.

Any feature that writes to YouTube, uploads videos, replies to comments, or modifies metadata will require more careful authentication and user approval.

Do not build autopublishing as the first MVP.

## Quota Considerations

Agents should be mindful that YouTube Data API calls use quota.

Do not repeatedly poll in a tight loop.

Prefer:

- Manual import for MVP.
- On-demand fetch.
- Caching comment results.
- Storing retrieved comment snapshots.
- Clear refresh buttons rather than background polling.

## Safe Automation Boundary

Good early automation:

```text
Fetch comments
Rank comments
Cluster themes
Run guardrail checks
Generate draft scripts
Generate descriptions
Generate prompts
Update local chain records
```

Avoid early automation:

```text
Autopublish without review
Auto-reply to comments without review
Delete or moderate comments automatically
Use private user data unnecessarily
Spam comment sections
Mass-upload generated videos
```

## Suggested Development Phases

### Phase 1: Manual MVP

- Paste selected comment manually.
- Generate next Short package.
- Store chain record.

### Phase 2: Assisted Comment Import

- Paste exported comments or JSON.
- Rank and cluster comments.
- Select top safe signal.

### Phase 3: API Read Integration

- Fetch comments by video ID.
- Cache comment snapshots.
- Select candidate comments.

### Phase 4: Creator Review Dashboard

- Show top comments.
- Show guardrail status.
- Show generated episode package.
- Bryan approves or edits.

### Phase 5: Optional Publishing Assistance

- Prepare metadata.
- Export upload package.
- Possibly integrate upload flow later with explicit review.

## Agent Guidance

Do not block MVP progress on YouTube API integration.

Build the creative loop first.

Automation should serve the audience-in-the-loop concept, not replace Bryan's review.
