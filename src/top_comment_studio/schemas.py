from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


SafetyStatus = Literal["approved", "approved_with_redirect", "needs_human_review", "rejected"]
EpisodeStatus = Literal["idea", "draft", "needs_review", "approved", "produced", "published", "archived", "rejected"]


class CommentInput(BaseModel):
    previous_video_title: str = Field(default="", max_length=140)
    previous_video_summary: str = Field(default="", max_length=1000)
    previous_video_cta: str = Field(default="", max_length=300)
    selected_comment: str = Field(min_length=1, max_length=2000)
    author_display_name: str = Field(default="", max_length=120)
    like_count: int = Field(default=0, ge=0)
    reply_count: int = Field(default=0, ge=0)
    selection_reason: str = Field(default="Top usable comment", max_length=500)
    creative_notes: str = Field(default="", max_length=1000)
    target_tone: str = Field(default="curious, cinematic, participatory", max_length=160)
    target_duration_seconds: int = Field(default=35, ge=15, le=60)
    visual_style: str = Field(default="vertical cinematic YouTube Short", max_length=240)


class GuardrailReview(BaseModel):
    status: SafetyStatus
    risk_categories: list[str] = Field(default_factory=list)
    reason: str
    safe_interpretation: str
    requires_bryan_review: bool = True


class WorkflowModelStack(BaseModel):
    llm_text_generation: str = "GPT 5.5"
    image_generation: str = "OpenAI Images 2.0"
    video_generation: str = "Seedance 2.0"
    runway_video_model_id: str = "seedance2"
    runway_image_model_id: str = "openai/gpt_image_2"
    workflow_registry_url: str


class ShortPackage(BaseModel):
    episode_id: str
    hook: str
    script: str
    voiceover: str
    visual_prompt: str
    video_prompt: str
    caption_text: str
    title_options: list[str]
    description: str
    pinned_comment: str
    next_cta: str
    thumbnail_idea: str
    safety_notes: str
    workflow_model_stack: WorkflowModelStack


class EpisodeRecord(BaseModel):
    episode_id: str
    series_id: str = "main"
    status: EpisodeStatus = "draft"
    title: str
    summary: str
    youtube_video_id: str = ""
    source_comment: dict[str, str | int]
    guardrail: GuardrailReview
    package: ShortPackage
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
