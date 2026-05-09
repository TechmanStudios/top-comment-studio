from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .guardrails import review_comment
from .package_generator import build_short_package
from .schemas import CommentInput, EpisodeRecord
from .settings import get_settings
from .storage import ChainStore


settings = get_settings()
PACKAGE_DIR = Path(__file__).parent
app = FastAPI(title=settings.app_name)
templates = Jinja2Templates(directory=str(PACKAGE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(PACKAGE_DIR / "static")), name="static")


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "runway_configured": settings.has_runway_secret,
    }


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "settings": settings,
            "latest": ChainStore(settings.data_dir).latest(),
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
    )
    record = create_episode_record(comment_input)
    saved_path = ChainStore(settings.data_dir).save(record)
    return templates.TemplateResponse(
        request=request,
        name="package.html",
        context={"request": request, "record": record, "saved_path": saved_path, "settings": settings},
    )


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
    )


def main() -> None:
    import uvicorn

    uvicorn.run("top_comment_studio.app:app", host="127.0.0.1", port=8000, reload=True)
