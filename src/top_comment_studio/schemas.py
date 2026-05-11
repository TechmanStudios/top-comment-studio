from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


SafetyStatus = Literal["approved", "approved_with_redirect", "needs_human_review", "rejected"]
EpisodeStatus = Literal[
    "idea", "draft", "needs_review", "approved", "produced", "published", "archived", "rejected"
]


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
    subject_focus: str = Field(default="", max_length=500)
    scene_world: str = Field(default="", max_length=500)
    motion_direction: str = Field(default="", max_length=500)
    camera_direction: str = Field(default="", max_length=500)
    audio_direction: str = Field(default="", max_length=500)
    quality_constraints: str = Field(default="", max_length=500)


class GuardrailReview(BaseModel):
    status: SafetyStatus
    risk_categories: list[str] = Field(default_factory=list)
    reason: str
    safe_interpretation: str
    requires_bryan_review: bool = True


class WorkflowModelStack(BaseModel):
    llm_text_generation: str = "GPT 5.5"
    image_generation: str = "Nano Banana Pro (Gemini 3 Pro Image)"
    video_generation: str = "Gen-4.5 shot studies + Veo 3.1 unified audio-video final"
    runway_video_model_id: str = "veo3.1"
    runway_image_model_id: str = "gemini_image3_pro"
    workflow_registry_url: str


class ProductionContext(BaseModel):
    previous_video_title: str = ""
    previous_video_summary: str = ""
    previous_video_cta: str = ""
    target_tone: str = "curious, cinematic, participatory"
    target_duration_seconds: int = 35
    visual_style: str = "vertical cinematic YouTube Short"
    creative_notes: str = ""
    subject_focus: str = ""
    scene_world: str = ""
    motion_direction: str = ""
    camera_direction: str = ""
    audio_direction: str = ""
    quality_constraints: str = ""


class RunwayWorkflowPreview(BaseModel):
    workflow_id: str = ""
    workflow_name: str = "TCS Gen/Veo Director v2"
    endpoint_path: str = ""
    duration_seconds: int = 12
    aspect_ratio: str = "1080:1920"
    logical_inputs: dict[str, str | int | bool] = Field(default_factory=dict)
    node_outputs: dict[str, dict[str, dict[str, Any]]] = Field(default_factory=dict)
    configuration_issues: list[str] = Field(default_factory=list)
    can_submit: bool = False


class RunwayWorkflowState(BaseModel):
    workflow_id: str = ""
    workflow_name: str = "TCS Gen/Veo Director v2"
    invocation_id: str = ""
    status: str = "not_submitted"
    progress: float | None = None
    output_urls: list[str] = Field(default_factory=list)
    failure: str = ""
    submitted_at: str = ""
    updated_at: str = ""
    last_response: dict[str, Any] = Field(default_factory=dict)


class RunwayDirectGenerationState(BaseModel):
    image_task_id: str = ""
    image_model: str = "gemini_image3_pro"
    image_ratio: str = "1536:2752"
    video_task_id: str = ""
    video_model: str = "gen4.5"
    video_ratio: str = "720:1280"
    duration_seconds: int = 5
    status: str = "not_submitted"
    progress: float | None = None
    image_output_urls: list[str] = Field(default_factory=list)
    output_urls: list[str] = Field(default_factory=list)
    failure: str = ""
    submitted_at: str = ""
    updated_at: str = ""
    last_response: dict[str, Any] = Field(default_factory=dict)


class RunwayImageBoardRowState(BaseModel):
    label: str = ""
    workflow_id: str = ""
    invocation_id: str = ""
    status: str = "not_submitted"
    progress: float | None = None
    output_urls: list[str] = Field(default_factory=list)
    failure: str = ""
    submitted_at: str = ""
    updated_at: str = ""
    last_response: dict[str, Any] = Field(default_factory=dict)


class RunwayImageBoardState(BaseModel):
    status: str = "not_submitted"
    rows: list[RunwayImageBoardRowState] = Field(default_factory=list)
    video_task_id: str = ""
    video_model: str = "veo3.1"
    video_ratio: str = "720:1280"
    video_duration_seconds: int = 10
    video_reference_image_url: str = ""
    video_status: str = "not_submitted"
    video_progress: float | None = None
    video_output_urls: list[str] = Field(default_factory=list)
    video_failure: str = ""
    submitted_at: str = ""
    updated_at: str = ""
    last_response: dict[str, Any] = Field(default_factory=dict)


class AudioVisualDirectorPacket(BaseModel):
    audience_signal: str = ""
    creator_intent: str = ""
    subject_focus: str = ""
    scene_world: str = ""
    visual_anchor: str = ""
    motion_arc: str = ""
    camera_language: str = ""
    audio_design: str = ""
    audio_visual_sync: str = ""
    negative_constraints: str = ""


class ShortPackage(BaseModel):
    episode_id: str
    hook: str
    script: str
    voiceover: str
    visual_prompt: str
    video_prompt: str
    av_director_packet: AudioVisualDirectorPacket = Field(default_factory=AudioVisualDirectorPacket)
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
    production_context: ProductionContext = Field(default_factory=ProductionContext)
    runway: RunwayWorkflowState = Field(default_factory=RunwayWorkflowState)
    runway_direct: RunwayDirectGenerationState = Field(default_factory=RunwayDirectGenerationState)
    runway_image_board: RunwayImageBoardState = Field(default_factory=RunwayImageBoardState)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
