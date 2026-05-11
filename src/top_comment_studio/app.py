from datetime import UTC, datetime
import mimetypes
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .guardrails import review_comment
from .package_generator import build_short_package
from .runway.client import (
    GEN45_CINEMATIC_DURATION_SECONDS,
    GEN45_VIDEO_MODEL,
    NANO_BANANA_PRO_HIGH_RES_PORTRAIT_RATIO,
    NANO_BANANA_PRO_MODEL,
    RUNWAY_VERTICAL_VIDEO_RATIO,
    VEO31_FINAL_VIDEO_DURATION_SECONDS,
    VEO31_VIDEO_MODEL,
    RunwayClient,
    RunwayClientError,
)
from .runway.workflows import (
    REQUIRED_WORKFLOW_INPUTS,
    build_logical_inputs,
    build_node_outputs,
    build_workflow_preview,
    parse_node_map,
    workflow_submission_blockers,
)
from .schemas import (
    CommentInput,
    EpisodeRecord,
    ProductionContext,
    RunwayDirectGenerationState,
    RunwayImageBoardRowState,
    RunwayImageBoardState,
    RunwayWorkflowState,
)
from .settings import get_settings
from .storage import ChainStore


settings = get_settings()
PACKAGE_DIR = Path(__file__).parent
mimetypes.add_type("text/css", ".css")
app = FastAPI(title=settings.app_name)
templates = Jinja2Templates(directory=str(PACKAGE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(PACKAGE_DIR / "static")), name="static")


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "runway_configured": settings.has_runway_secret,
        "runway_workflow_configured": settings.has_runway_workflow_id,
    }


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    latest = ChainStore(settings.data_dir).latest()
    latest_rendered_video_urls = rendered_video_urls(latest) if latest else []
    latest_render_progress = render_progress(latest)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "settings": settings,
            "latest": latest,
            "latest_rendered_video_urls": latest_rendered_video_urls,
            "latest_render_progress_percent": format_progress_percent(latest_render_progress),
            "latest_render_progress_width": format_progress_width(latest_render_progress),
            "latest_render_status_label": render_status_label(latest),
        },
    )


@app.post("/package", response_class=HTMLResponse)
def create_package_view(
    request: Request,
    selected_comment: str = Form(...),
    previous_video_title: str = Form(""),
    previous_video_summary: str = Form(""),
    previous_video_cta: str = Form(""),
    author_display_name: str = Form(""),
    like_count: int = Form(0),
    reply_count: int = Form(0),
    selection_reason: str = Form("Top usable comment"),
    creative_notes: str = Form(""),
    target_tone: str = Form("curious, cinematic, participatory"),
    target_duration_seconds: int = Form(35),
    visual_style: str = Form("vertical cinematic YouTube Short"),
    subject_focus: str = Form(""),
    scene_world: str = Form(""),
    motion_direction: str = Form(""),
    camera_direction: str = Form(""),
    audio_direction: str = Form(""),
    quality_constraints: str = Form(""),
) -> HTMLResponse:
    comment_input = CommentInput(
        previous_video_title=previous_video_title,
        previous_video_summary=previous_video_summary,
        previous_video_cta=previous_video_cta,
        selected_comment=selected_comment,
        author_display_name=author_display_name,
        like_count=like_count,
        reply_count=reply_count,
        selection_reason=selection_reason,
        creative_notes=creative_notes,
        target_tone=target_tone,
        target_duration_seconds=target_duration_seconds,
        visual_style=visual_style,
        subject_focus=subject_focus,
        scene_world=scene_world,
        motion_direction=motion_direction,
        camera_direction=camera_direction,
        audio_direction=audio_direction,
        quality_constraints=quality_constraints,
    )
    store = ChainStore(settings.data_dir)
    record = create_episode_record(comment_input)
    record, runway_message, runway_error = submit_record_to_runway(
        record,
        creator_approved=True,
    )
    saved_path = store.save(record)
    return render_package_response(
        request,
        record,
        saved_path,
        runway_message=runway_message,
        runway_error=runway_error,
    )


@app.get("/package/{episode_id}", response_class=HTMLResponse)
def package_view(request: Request, episode_id: str) -> HTMLResponse:
    store = ChainStore(settings.data_dir)
    record = get_episode_or_404(store, episode_id)
    return render_package_response(request, record, store.path_for(episode_id))


@app.post("/package/{episode_id}/submit-runway", response_class=HTMLResponse)
def submit_runway_workflow(
    request: Request,
    episode_id: str,
    creator_approved: bool = Form(False),
) -> HTMLResponse:
    store = ChainStore(settings.data_dir)
    record = get_episode_or_404(store, episode_id)
    record, runway_message, runway_error = submit_record_to_runway(
        record,
        creator_approved=creator_approved,
    )
    saved_path = store.save(record)
    return render_package_response(
        request,
        record,
        saved_path,
        runway_message=runway_message,
        runway_error=runway_error,
    )


def submit_record_to_runway(
    record: EpisodeRecord,
    *,
    creator_approved: bool,
    client: RunwayClient | None = None,
) -> tuple[EpisodeRecord, str, str]:
    preview = build_workflow_preview(record, settings)
    blockers = workflow_submission_blockers(
        record,
        preview,
        has_runway_secret=settings.has_runway_secret,
        creator_approved=creator_approved,
    )
    if blockers:
        failure = " ".join(blockers)
        record.runway = RunwayWorkflowState(
            workflow_id=preview.workflow_id,
            workflow_name=preview.workflow_name,
            status="failed",
            failure=failure,
            updated_at=current_timestamp(),
        )
        return record, "", failure

    now = current_timestamp()
    try:
        runway_client = client or RunwayClient(settings)
        response = runway_client.run_workflow(preview.workflow_id, preview.node_outputs)
    except RunwayClientError as exc:
        record.runway = RunwayWorkflowState(
            workflow_id=preview.workflow_id,
            workflow_name=preview.workflow_name,
            status="failed",
            failure=str(exc),
            updated_at=now,
            last_response={"status_code": exc.status_code, "response_body": exc.response_body},
        )
        return record, "", str(exc)

    invocation_id = str(response.get("id") or response.get("workflowInvocationId") or "")
    status = "submitted" if invocation_id else "failed"
    failure = "" if invocation_id else "Runway did not return a workflow invocation ID."
    record.runway = RunwayWorkflowState(
        workflow_id=preview.workflow_id,
        workflow_name=preview.workflow_name,
        invocation_id=invocation_id,
        status=status,
        failure=failure,
        submitted_at=now,
        updated_at=now,
        last_response=response,
    )
    message = f"Submitted to Runway invocation {invocation_id}." if invocation_id else failure
    return record, message if invocation_id else "", failure


@app.get("/package/{episode_id}/runway-status", response_class=HTMLResponse)
def runway_status(request: Request, episode_id: str) -> HTMLResponse:
    store = ChainStore(settings.data_dir)
    record = get_episode_or_404(store, episode_id)
    if not record.runway.invocation_id:
        return render_package_response(
            request,
            record,
            store.path_for(episode_id),
            runway_error="No Runway invocation has been submitted for this package yet.",
        )
    if not settings.has_runway_secret:
        return render_package_response(
            request,
            record,
            store.path_for(episode_id),
            runway_error="Set RUNWAYML_HACKATHON_API_SECRET before refreshing Runway status.",
        )

    now = current_timestamp()
    try:
        response = RunwayClient(settings).retrieve_workflow_invocation(record.runway.invocation_id)
    except RunwayClientError as exc:
        record.runway = record.runway.model_copy(
            update={
                "status": "failed",
                "failure": str(exc),
                "updated_at": now,
                "last_response": {
                    "status_code": exc.status_code,
                    "response_body": exc.response_body,
                },
            }
        )
        saved_path = store.save(record)
        return render_package_response(request, record, saved_path, runway_error=str(exc))

    record.runway = record.runway.model_copy(
        update={
            "status": str(response.get("status", "unknown")),
            "progress": extract_progress(response),
            "output_urls": extract_output_urls(response),
            "failure": extract_failure(response),
            "updated_at": now,
            "last_response": response,
        }
    )
    saved_path = store.save(record)
    return render_package_response(
        request, record, saved_path, runway_message="Runway status refreshed."
    )


@app.post("/package/{episode_id}/submit-runway-direct", response_class=HTMLResponse)
def submit_direct_runway_generation(
    request: Request,
    episode_id: str,
    creator_approved: bool = Form(False),
) -> HTMLResponse:
    store = ChainStore(settings.data_dir)
    record = get_episode_or_404(store, episode_id)
    blockers = direct_generation_blockers(
        record,
        has_runway_secret=settings.has_runway_secret,
        creator_approved=creator_approved,
    )
    if blockers:
        return render_package_response(
            request,
            record,
            store.path_for(episode_id),
            direct_runway_error=" ".join(blockers),
        )

    now = current_timestamp()
    try:
        response = RunwayClient(settings).create_text_to_image_task(
            build_direct_image_prompt(record)
        )
    except RunwayClientError as exc:
        record.runway_direct = RunwayDirectGenerationState(
            status="failed",
            failure=str(exc),
            updated_at=now,
            last_response={"status_code": exc.status_code, "response_body": exc.response_body},
        )
        saved_path = store.save(record)
        return render_package_response(request, record, saved_path, direct_runway_error=str(exc))

    image_task_id = str(response.get("id", ""))
    status = "image_submitted" if image_task_id else "failed"
    failure = "" if image_task_id else "Runway did not return a Nano Banana image task ID."
    record.runway_direct = RunwayDirectGenerationState(
        image_task_id=image_task_id,
        image_model=NANO_BANANA_PRO_MODEL,
        image_ratio=NANO_BANANA_PRO_HIGH_RES_PORTRAIT_RATIO,
        video_model=GEN45_VIDEO_MODEL,
        video_ratio=RUNWAY_VERTICAL_VIDEO_RATIO,
        duration_seconds=GEN45_CINEMATIC_DURATION_SECONDS,
        status=status,
        failure=failure,
        submitted_at=now,
        updated_at=now,
        last_response=response,
    )
    saved_path = store.save(record)
    message = f"Submitted Nano Banana image task {image_task_id}." if image_task_id else failure
    return render_package_response(request, record, saved_path, direct_runway_message=message)


@app.get("/package/{episode_id}/runway-direct-status", response_class=HTMLResponse)
def runway_direct_status(request: Request, episode_id: str) -> HTMLResponse:
    store = ChainStore(settings.data_dir)
    record = get_episode_or_404(store, episode_id)
    if not record.runway_direct.image_task_id and not record.runway_direct.video_task_id:
        return render_package_response(
            request,
            record,
            store.path_for(episode_id),
            direct_runway_error="No direct Runway generation has been submitted for this package yet.",
        )
    if not settings.has_runway_secret:
        return render_package_response(
            request,
            record,
            store.path_for(episode_id),
            direct_runway_error="Set RUNWAYML_HACKATHON_API_SECRET before refreshing direct Runway status.",
        )

    now = current_timestamp()
    client = RunwayClient(settings)
    try:
        record = advance_direct_generation(record, client, now)
    except RunwayClientError as exc:
        record.runway_direct = record.runway_direct.model_copy(
            update={
                "status": "failed",
                "failure": str(exc),
                "updated_at": now,
                "last_response": {
                    "status_code": exc.status_code,
                    "response_body": exc.response_body,
                },
            }
        )
        saved_path = store.save(record)
        return render_package_response(request, record, saved_path, direct_runway_error=str(exc))

    saved_path = store.save(record)
    return render_package_response(
        request,
        record,
        saved_path,
        direct_runway_message="Direct Runway status refreshed.",
    )


@app.post("/package/{episode_id}/submit-runway-image-board", response_class=HTMLResponse)
def submit_runway_image_board(
    request: Request,
    episode_id: str,
    creator_approved: bool = Form(False),
) -> HTMLResponse:
    store = ChainStore(settings.data_dir)
    record = get_episode_or_404(store, episode_id)
    blockers = image_board_submission_blockers(
        record,
        has_runway_secret=settings.has_runway_secret,
        creator_approved=creator_approved,
    )
    if blockers:
        return render_package_response(
            request,
            record,
            store.path_for(episode_id),
            image_board_error=" ".join(blockers),
        )

    now = current_timestamp()
    node_outputs, issues = build_image_board_node_outputs(record)
    if issues:
        return render_package_response(
            request,
            record,
            store.path_for(episode_id),
            image_board_error=" ".join(issues),
        )

    rows: list[RunwayImageBoardRowState] = []
    client = RunwayClient(settings)
    for label, workflow_id in settings.runway_image_board_workflow_ids.items():
        try:
            response = client.run_workflow(workflow_id, node_outputs)
        except RunwayClientError as exc:
            rows.append(
                RunwayImageBoardRowState(
                    label=label,
                    workflow_id=workflow_id,
                    status="failed",
                    failure=str(exc),
                    updated_at=now,
                    last_response={
                        "status_code": exc.status_code,
                        "response_body": exc.response_body,
                    },
                )
            )
            continue

        invocation_id = str(response.get("id") or response.get("workflowInvocationId") or "")
        rows.append(
            RunwayImageBoardRowState(
                label=label,
                workflow_id=workflow_id,
                invocation_id=invocation_id,
                status="submitted" if invocation_id else "failed",
                failure="" if invocation_id else "Runway did not return a board row invocation ID.",
                submitted_at=now,
                updated_at=now,
                last_response=response,
            )
        )

    record.runway_image_board = RunwayImageBoardState(
        status=aggregate_image_board_status(rows),
        rows=rows,
        video_model=VEO31_VIDEO_MODEL,
        video_ratio=RUNWAY_VERTICAL_VIDEO_RATIO,
        video_duration_seconds=VEO31_FINAL_VIDEO_DURATION_SECONDS,
        submitted_at=now,
        updated_at=now,
    )
    saved_path = store.save(record)
    return render_package_response(
        request,
        record,
        saved_path,
        image_board_message="Submitted the three image-board row workflows.",
    )


@app.get("/package/{episode_id}/runway-image-board-status", response_class=HTMLResponse)
def runway_image_board_status(request: Request, episode_id: str) -> HTMLResponse:
    store = ChainStore(settings.data_dir)
    record = get_episode_or_404(store, episode_id)
    if not record.runway_image_board.rows and not record.runway_image_board.video_task_id:
        return render_package_response(
            request,
            record,
            store.path_for(episode_id),
            image_board_error="No image-board workflow has been submitted for this package yet.",
        )
    if not settings.has_runway_secret:
        return render_package_response(
            request,
            record,
            store.path_for(episode_id),
            image_board_error="Set RUNWAYML_HACKATHON_API_SECRET before refreshing the image board.",
        )

    now = current_timestamp()
    try:
        record = advance_image_board_generation(record, RunwayClient(settings), now)
    except RunwayClientError as exc:
        record.runway_image_board = record.runway_image_board.model_copy(
            update={
                "status": "failed",
                "updated_at": now,
                "last_response": {
                    "status_code": exc.status_code,
                    "response_body": exc.response_body,
                },
            }
        )
        saved_path = store.save(record)
        return render_package_response(request, record, saved_path, image_board_error=str(exc))

    saved_path = store.save(record)
    return render_package_response(
        request,
        record,
        saved_path,
        image_board_message="Image-board status refreshed.",
    )


@app.post("/package/{episode_id}/submit-runway-image-board-video", response_class=HTMLResponse)
def submit_runway_image_board_video(
    request: Request,
    episode_id: str,
    creator_approved: bool = Form(False),
) -> HTMLResponse:
    store = ChainStore(settings.data_dir)
    record = get_episode_or_404(store, episode_id)
    blockers = image_board_video_submission_blockers(
        record,
        has_runway_secret=settings.has_runway_secret,
        creator_approved=creator_approved,
    )
    if blockers:
        return render_package_response(
            request,
            record,
            store.path_for(episode_id),
            image_board_error=" ".join(blockers),
        )

    now = current_timestamp()
    image_urls = collect_image_board_image_urls(record.runway_image_board)
    reference_image_url = select_hero_reference_image(image_urls)
    try:
        response = RunwayClient(settings).create_image_to_video_task(
            build_veo31_final_video_prompt(record),
            reference_image_url,
            model=record.runway_image_board.video_model or VEO31_VIDEO_MODEL,
            ratio=record.runway_image_board.video_ratio or RUNWAY_VERTICAL_VIDEO_RATIO,
            duration=record.runway_image_board.video_duration_seconds,
        )
    except RunwayClientError as exc:
        record.runway_image_board = record.runway_image_board.model_copy(
            update={
                "video_status": "failed",
                "video_failure": str(exc),
                "updated_at": now,
                "last_response": {
                    "status_code": exc.status_code,
                    "response_body": exc.response_body,
                },
            }
        )
        saved_path = store.save(record)
        return render_package_response(request, record, saved_path, image_board_error=str(exc))

    video_task_id = str(response.get("id", ""))
    record.runway_image_board = record.runway_image_board.model_copy(
        update={
            "video_task_id": video_task_id,
            "video_status": "video_submitted" if video_task_id else "failed",
            "video_progress": extract_progress(response),
            "video_failure": ""
            if video_task_id
            else "Runway did not return a Veo 3.1 video task ID.",
            "video_reference_image_url": reference_image_url,
            "updated_at": now,
            "last_response": response,
        }
    )
    saved_path = store.save(record)
    message = (
        f"Submitted Veo 3.1 final video task {video_task_id}."
        if video_task_id
        else "Runway did not return a Veo 3.1 video task ID."
    )
    return render_package_response(request, record, saved_path, image_board_message=message)


@app.post("/api/package", response_model=EpisodeRecord)
def create_package_api(comment_input: CommentInput) -> EpisodeRecord:
    record = create_episode_record(comment_input)
    ChainStore(settings.data_dir).save(record)
    return record


def create_episode_record(comment_input: CommentInput) -> EpisodeRecord:
    store = ChainStore(settings.data_dir)
    episode_id = store.next_episode_id()
    guardrail = review_comment(comment_input)
    package = build_short_package(episode_id, comment_input, guardrail, settings)
    return EpisodeRecord(
        episode_id=episode_id,
        title=package.title_options[0],
        summary=guardrail.safe_interpretation,
        source_comment={
            "text": comment_input.selected_comment,
            "author": comment_input.author_display_name,
            "likes": comment_input.like_count,
            "replies": comment_input.reply_count,
            "selection_reason": comment_input.selection_reason,
        },
        guardrail=guardrail,
        package=package,
        production_context=ProductionContext(
            previous_video_title=comment_input.previous_video_title,
            previous_video_summary=comment_input.previous_video_summary,
            previous_video_cta=comment_input.previous_video_cta,
            target_tone=comment_input.target_tone,
            target_duration_seconds=comment_input.target_duration_seconds,
            visual_style=comment_input.visual_style,
            creative_notes=comment_input.creative_notes,
            subject_focus=comment_input.subject_focus,
            scene_world=comment_input.scene_world,
            motion_direction=comment_input.motion_direction,
            camera_direction=comment_input.camera_direction,
            audio_direction=comment_input.audio_direction,
            quality_constraints=comment_input.quality_constraints,
        ),
    )


def get_episode_or_404(store: ChainStore, episode_id: str) -> EpisodeRecord:
    record = store.get(episode_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Episode record not found")
    return record


def render_package_response(
    request: Request,
    record: EpisodeRecord,
    saved_path: Path,
    *,
    runway_message: str = "",
    runway_error: str = "",
    direct_runway_message: str = "",
    direct_runway_error: str = "",
    image_board_message: str = "",
    image_board_error: str = "",
) -> HTMLResponse:
    image_board_urls = collect_image_board_output_urls(record.runway_image_board)
    image_board_video_urls = record.runway_image_board.video_output_urls
    return templates.TemplateResponse(
        request=request,
        name="package.html",
        context={
            "request": request,
            "record": record,
            "saved_path": saved_path,
            "settings": settings,
            "rendered_video_urls": rendered_video_urls(record),
            "render_status_label": render_status_label(record),
            "render_progress_percent": format_progress_percent(render_progress(record)),
            "render_progress_width": format_progress_width(render_progress(record)),
            "runway_preview": build_workflow_preview(record, settings),
            "direct_can_submit": direct_generation_can_submit(record),
            "runway_progress_percent": format_progress_percent(record.runway.progress),
            "runway_progress_width": format_progress_width(record.runway.progress),
            "runway_asset_counts": summarize_asset_counts(record.runway.output_urls),
            "direct_progress_percent": format_progress_percent(record.runway_direct.progress),
            "direct_progress_width": format_progress_width(record.runway_direct.progress),
            "direct_asset_counts": summarize_asset_counts(record.runway_direct.output_urls),
            "image_board_can_submit": image_board_can_submit(record),
            "image_board_configuration_issues": image_board_configuration_issues(),
            "image_board_row_views": image_board_row_views(record.runway_image_board),
            "image_board_image_urls": collect_image_board_image_urls(record.runway_image_board),
            "image_board_asset_counts": summarize_asset_counts(image_board_urls),
            "image_board_video_progress_percent": format_progress_percent(
                record.runway_image_board.video_progress
            ),
            "image_board_video_progress_width": format_progress_width(
                record.runway_image_board.video_progress
            ),
            "image_board_video_asset_counts": summarize_asset_counts(image_board_video_urls),
            "runway_message": runway_message,
            "runway_error": runway_error,
            "direct_runway_message": direct_runway_message,
            "direct_runway_error": direct_runway_error,
            "image_board_message": image_board_message,
            "image_board_error": image_board_error,
        },
    )


def rendered_video_urls(record: EpisodeRecord) -> list[str]:
    return (
        record.runway.output_urls
        or record.runway_image_board.video_output_urls
        or record.runway_direct.output_urls
    )


def render_progress(record: EpisodeRecord | None) -> float | None:
    if record is None:
        return None
    if rendered_video_urls(record):
        return 1.0
    if record.runway.progress is not None:
        return record.runway.progress
    if record.runway.invocation_id:
        return 0.05
    if record.runway_image_board.video_progress is not None:
        return record.runway_image_board.video_progress
    if record.runway_direct.progress is not None:
        return record.runway_direct.progress
    return 0.0


def render_status_label(record: EpisodeRecord | None) -> str:
    if record is None:
        return "No render queued"
    if rendered_video_urls(record):
        return "Render ready"
    if record.runway.failure:
        return "Render blocked"
    if record.runway.invocation_id:
        return "Rendering"
    return "Awaiting render"


def direct_generation_can_submit(record: EpisodeRecord) -> bool:
    return settings.has_runway_secret and record.guardrail.status != "rejected"


def direct_generation_blockers(
    record: EpisodeRecord,
    *,
    has_runway_secret: bool,
    creator_approved: bool,
) -> list[str]:
    blockers: list[str] = []
    if not creator_approved:
        blockers.append("Creator approval is required before submitting direct Runway generation.")
    if not has_runway_secret:
        blockers.append("Set RUNWAYML_HACKATHON_API_SECRET before submitting to Runway.")
    if record.guardrail.status == "rejected":
        blockers.append("Rejected comments cannot be submitted to Runway.")
    return blockers


def image_board_can_submit(record: EpisodeRecord) -> bool:
    return (
        settings.has_runway_secret
        and settings.has_runway_image_board_workflows
        and record.guardrail.status != "rejected"
    )


def image_board_submission_blockers(
    record: EpisodeRecord,
    *,
    has_runway_secret: bool,
    creator_approved: bool,
) -> list[str]:
    blockers: list[str] = []
    if not creator_approved:
        blockers.append("Creator approval is required before submitting the image board.")
    if not has_runway_secret:
        blockers.append("Set RUNWAYML_HACKATHON_API_SECRET before submitting to Runway.")
    if record.guardrail.status == "rejected":
        blockers.append("Rejected comments cannot be submitted to Runway.")
    blockers.extend(image_board_configuration_issues())
    return blockers


def image_board_video_submission_blockers(
    record: EpisodeRecord,
    *,
    has_runway_secret: bool,
    creator_approved: bool,
) -> list[str]:
    blockers: list[str] = []
    if not creator_approved:
        blockers.append("Creator approval is required before creating the Veo 3.1 final video.")
    if not has_runway_secret:
        blockers.append("Set RUNWAYML_HACKATHON_API_SECRET before submitting to Runway.")
    if record.guardrail.status == "rejected":
        blockers.append("Rejected comments cannot be submitted to Runway.")
    image_urls = collect_image_board_image_urls(record.runway_image_board)
    if len(image_urls) < 9:
        blockers.append(
            "Generate and refresh all nine image-board outputs before creating the Veo 3.1 final video."
        )
    return blockers


def image_board_configuration_issues() -> list[str]:
    issues: list[str] = []
    if not settings.has_runway_image_board_workflows:
        issues.append(
            "Set RUNWAY_IMAGE_BOARD_ROW_1_WORKFLOW_ID, "
            "RUNWAY_IMAGE_BOARD_ROW_2_WORKFLOW_ID, and "
            "RUNWAY_IMAGE_BOARD_ROW_3_WORKFLOW_ID."
        )

    node_map, node_map_issues = parse_node_map(settings.runway_workflow_node_map_json)
    issues.extend(node_map_issues)
    missing_inputs = [name for name in REQUIRED_WORKFLOW_INPUTS if name not in node_map]
    if missing_inputs:
        issues.append("Map workflow input nodes for: " + ", ".join(missing_inputs))
    return issues


def build_image_board_node_outputs(
    record: EpisodeRecord,
) -> tuple[dict[str, dict[str, dict[str, Any]]], list[str]]:
    issues = image_board_configuration_issues()
    if issues:
        return {}, issues
    node_map, _ = parse_node_map(settings.runway_workflow_node_map_json)
    return build_node_outputs(build_logical_inputs(record), node_map), []


def image_board_row_views(board: RunwayImageBoardState) -> list[dict[str, Any]]:
    views: list[dict[str, Any]] = []
    for row in board.rows:
        views.append(
            {
                "label": row.label,
                "workflow_id": row.workflow_id,
                "invocation_id": row.invocation_id,
                "status": row.status,
                "progress_percent": format_progress_percent(row.progress),
                "progress_width": format_progress_width(row.progress),
                "asset_counts": summarize_asset_counts(row.output_urls),
                "output_urls": row.output_urls,
                "failure": row.failure,
            }
        )
    return views


def advance_image_board_generation(
    record: EpisodeRecord, client: RunwayClient, now: str
) -> EpisodeRecord:
    board = record.runway_image_board
    rows: list[RunwayImageBoardRowState] = []
    for row in board.rows:
        if not row.invocation_id:
            rows.append(row)
            continue
        response = client.retrieve_workflow_invocation(row.invocation_id)
        rows.append(
            row.model_copy(
                update={
                    "status": str(response.get("status", "unknown")),
                    "progress": extract_progress(response),
                    "output_urls": extract_output_urls(response),
                    "failure": extract_failure(
                        response,
                        missing_output_message=f"{row.label} returned SUCCEEDED without image outputs.",
                    ),
                    "updated_at": now,
                    "last_response": response,
                }
            )
        )

    update: dict[str, Any] = {
        "rows": rows,
        "status": aggregate_image_board_status(rows),
        "updated_at": now,
    }
    if board.video_task_id:
        video_response = client.retrieve_task(board.video_task_id)
        update.update(
            {
                "video_status": str(video_response.get("status", "unknown")),
                "video_progress": extract_progress(video_response),
                "video_output_urls": extract_output_urls(video_response),
                "video_failure": extract_failure(
                    video_response,
                    missing_output_message=(
                        "Veo 3.1 returned SUCCEEDED without a final video output."
                    ),
                ),
                "last_response": video_response,
            }
        )
    record.runway_image_board = board.model_copy(update=update)
    return record


def aggregate_image_board_status(rows: list[RunwayImageBoardRowState]) -> str:
    if not rows:
        return "not_submitted"
    statuses = [row.status.upper() for row in rows]
    if any(row.failure for row in rows) or any(status in failed_statuses() for status in statuses):
        return "failed"
    if all(
        status == "SUCCEEDED" and len(row.output_urls) >= 3
        for status, row in zip(statuses, rows, strict=True)
    ):
        return "images_ready"
    if any(status in active_statuses() for status in statuses):
        return "running"
    return "submitted"


def collect_image_board_output_urls(board: RunwayImageBoardState) -> list[str]:
    urls: list[str] = []
    for row in board.rows:
        urls.extend(row.output_urls)
    return urls


def collect_image_board_image_urls(board: RunwayImageBoardState) -> list[str]:
    image_urls: list[str] = []
    for url in collect_image_board_output_urls(board):
        path = urlparse(url).path.lower()
        if path.endswith((".png", ".jpg", ".jpeg", ".webp")):
            image_urls.append(url)
    return image_urls


def active_statuses() -> set[str]:
    return {"SUBMITTED", "PENDING", "RUNNING", "THROTTLED", "STARTING", "PROCESSING"}


def failed_statuses() -> set[str]:
    return {"FAILED", "CANCELED", "CANCELLED"}


def build_direct_image_prompt(record: EpisodeRecord) -> str:
    packet = record.package.av_director_packet
    return compact_prompt(
        " ".join(
            [
                "Portrait 9:16 first-frame reference for a safe original Gen/Veo YouTube Short.",
                "No text overlays, no logos, no real-person likeness, and no copyrighted characters.",
                record.package.visual_prompt,
                f"Visual anchor: {packet.visual_anchor}.",
                f"Subject continuity: {packet.subject_focus}.",
                f"Scene world: {packet.scene_world}.",
                f"Audience comment: {record.source_comment.get('text', '')}.",
                f"Safe interpretation: {record.guardrail.safe_interpretation}.",
                "Create one readable cinematic still with a clear opening silhouette.",
            ]
        ),
        max_chars=950,
    )


def build_direct_gen45_prompt(record: EpisodeRecord) -> str:
    packet = record.package.av_director_packet
    return compact_prompt(
        " ".join(
            [
                "Gen-4.5 silent cinematic shot study from a unified audio-video director packet. Use the supplied first frame as the exact opening image.",
                record.package.video_prompt,
                f"Visual anchor: {packet.visual_anchor}.",
                f"Motion arc: {packet.motion_arc}.",
                f"Camera language: {packet.camera_language}.",
                "Treat audio cues as timing rhythm only; this Gen-4.5 study may be silent.",
                build_unified_av_context(record),
                f"Final beat: {record.package.next_cta}",
                "Keep it safe, fictional, logo-free, text-free, and vertical.",
            ]
        ),
        max_chars=950,
    )


def build_veo31_final_video_prompt(record: EpisodeRecord) -> str:
    packet = record.package.av_director_packet
    return compact_prompt(
        " ".join(
            [
                "Veo 3.1 final vertical video with native audio from one unified audio-video director packet. Use the supplied first-frame board image as the opening visual anchor.",
                "Preserve the nine-image board plan: hook frame, hero subject, setting, palette, texture, action pose, transition twist, payoff reveal, thumbnail beat.",
                f"Audio design: {packet.audio_design}.",
                f"Audio-video sync: {packet.audio_visual_sync}.",
                record.package.video_prompt,
                build_unified_av_context(record),
                f"Final beat: {record.package.next_cta}",
            ]
        ),
        max_chars=950,
    )


def build_unified_av_context(record: EpisodeRecord) -> str:
    context = record.production_context
    packet = record.package.av_director_packet
    return " ".join(
        [
            f"AV packet: episode {record.episode_id}; safety {record.guardrail.status}; aspect 1080:1920.",
            f"Audience signal: {packet.audience_signal or record.source_comment.get('text', '')}.",
            f"Creator intent: {packet.creator_intent}.",
            f"Subject: {packet.subject_focus}. World: {packet.scene_world}.",
            f"Negative constraints: {packet.negative_constraints}.",
            f"Continuity: previous summary {context.previous_video_summary}; previous CTA {context.previous_video_cta}; next CTA {record.package.next_cta}.",
        ]
    )


def select_hero_reference_image(image_urls: list[str]) -> str:
    return image_urls[0]


def compact_prompt(prompt: str, *, max_chars: int) -> str:
    normalized = " ".join(prompt.split())
    if len(normalized) <= max_chars:
        return normalized
    return normalized[:max_chars].rsplit(" ", 1)[0].rstrip(" .,;") + "."


def advance_direct_generation(
    record: EpisodeRecord, client: RunwayClient, now: str
) -> EpisodeRecord:
    direct = record.runway_direct
    if direct.video_task_id:
        response = client.retrieve_task(direct.video_task_id)
        record.runway_direct = direct.model_copy(
            update={
                "status": str(response.get("status", "unknown")),
                "progress": extract_progress(response),
                "output_urls": extract_output_urls(response),
                "failure": extract_failure(
                    response,
                    missing_output_message=(
                        "Gen-4.5 returned SUCCEEDED without a cinematic shot output URL."
                    ),
                ),
                "updated_at": now,
                "last_response": response,
            }
        )
        return record

    image_response = client.retrieve_task(direct.image_task_id)
    image_status = str(image_response.get("status", "unknown"))
    image_urls = extract_output_urls(image_response)
    image_failure = extract_failure(
        image_response,
        missing_output_message="Nano Banana returned SUCCEEDED without an image output URL.",
    )
    direct = direct.model_copy(
        update={
            "status": image_status,
            "progress": extract_progress(image_response),
            "image_output_urls": image_urls,
            "failure": image_failure,
            "updated_at": now,
            "last_response": image_response,
        }
    )
    record.runway_direct = direct

    if image_status.upper() != "SUCCEEDED" or image_failure:
        return record

    video_response = client.create_image_to_video_task(
        build_direct_gen45_prompt(record),
        image_urls[0],
        model=direct.video_model or GEN45_VIDEO_MODEL,
        ratio=direct.video_ratio or RUNWAY_VERTICAL_VIDEO_RATIO,
        duration=direct.duration_seconds,
    )
    video_task_id = str(video_response.get("id", ""))
    record.runway_direct = direct.model_copy(
        update={
            "video_task_id": video_task_id,
            "status": "video_submitted" if video_task_id else "failed",
            "progress": extract_progress(video_response),
            "failure": "" if video_task_id else "Runway did not return a Gen-4.5 video task ID.",
            "updated_at": now,
            "last_response": {"image_task": image_response, "video_task": video_response},
        }
    )
    return record


def current_timestamp() -> str:
    return datetime.now(UTC).isoformat()


def extract_output_urls(value: Any) -> list[str]:
    urls: list[str] = []
    collect_urls(value.get("output", value) if isinstance(value, dict) else value, urls)
    return urls


def extract_progress(response: dict[str, Any]) -> float | None:
    progress = response.get("progress")
    if not isinstance(progress, int | float):
        return None
    return min(max(float(progress), 0.0), 1.0)


def format_progress_percent(progress: float | None) -> str:
    if progress is None:
        return ""
    return f"{progress * 100:.1f}%"


def format_progress_width(progress: float | None) -> str:
    if progress is None:
        return "0%"
    return f"{progress * 100:.1f}%"


def summarize_asset_counts(urls: list[str]) -> dict[str, int]:
    counts = {"video": 0, "audio": 0, "image": 0, "other": 0}
    for url in urls:
        path = urlparse(url).path.lower()
        if path.endswith(".mp4"):
            counts["video"] += 1
        elif path.endswith(".mp3"):
            counts["audio"] += 1
        elif path.endswith((".png", ".jpg", ".jpeg", ".webp")):
            counts["image"] += 1
        else:
            counts["other"] += 1
    return {label: count for label, count in counts.items() if count}


def collect_urls(value: Any, urls: list[str]) -> None:
    if isinstance(value, str):
        if value.startswith(("https://", "runway://")):
            urls.append(value)
        return
    if isinstance(value, dict):
        for child in value.values():
            collect_urls(child, urls)
        return
    if isinstance(value, list):
        for child in value:
            collect_urls(child, urls)


def extract_failure(
    response: dict[str, Any],
    *,
    missing_output_message: str = (
        "Runway returned SUCCEEDED without exposed workflow outputs. "
        "Confirm the final video output is selected and every upstream node feeding it "
        "produces a value."
    ),
) -> str:
    failure = response.get("failure") or response.get("failureCode") or ""
    if isinstance(failure, str):
        if failure:
            return failure
    elif failure:
        return str(failure)

    status = str(response.get("status", "")).upper()
    node_errors = response.get("nodeErrors")
    messages: list[str] = []
    if isinstance(node_errors, dict):
        for node_error in node_errors.values():
            if not isinstance(node_error, dict):
                messages.append(str(node_error))
                continue
            node_name = str(node_error.get("nodeName") or "Unknown node")
            message = str(node_error.get("message") or "Node error")
            if status == "SUCCEEDED" and message == "Node is already running in this execution":
                continue
            if "No model variant mapping" in message and "gpt-tidepool-alpha" in message:
                message = (
                    f"{message}. GPT Image 2 workflow nodes are not API-safe here; "
                    "use Nano Banana Pro via gemini_image3_pro, with gemini_2.5_flash "
                    "as the fast Nano Banana fallback, before routing images into Gen-4.5 or Veo 3.1."
                )
            messages.append(f"{node_name}: {message}")

    if messages:
        return "Node errors: " + "; ".join(messages)

    if status == "SUCCEEDED" and not response.get("output"):
        return missing_output_message

    return ""


def main() -> None:
    import uvicorn

    uvicorn.run("top_comment_studio.app:app", host="127.0.0.1", port=8000, reload=True)
