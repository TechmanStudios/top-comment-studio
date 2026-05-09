from .schemas import CommentInput, GuardrailReview, ShortPackage, WorkflowModelStack
from .settings import Settings


def build_short_package(
    episode_id: str,
    comment_input: CommentInput,
    guardrail: GuardrailReview,
    settings: Settings,
) -> ShortPackage:
    creative_seed = guardrail.safe_interpretation
    tone = comment_input.target_tone
    duration = comment_input.target_duration_seconds
    visual_style = comment_input.visual_style

    title_subject = _compact_subject(comment_input.selected_comment)
    hook = f"Top comment sent the AI here: {title_subject}."
    next_cta = "Top safe comment decides what the AI changes next."

    script = " ".join(
        [
            hook,
            f"The community's idea becomes today's design brief: {creative_seed}",
            "First, the AI turns the request into a visual plan.",
            "Then it builds the most cinematic version that still keeps Bryan in the approval loop.",
            "Now the next move goes back to the audience.",
            next_cta,
        ]
    )

    visual_prompt = (
        f"Create storyboard reference imagery for a {duration}-second vertical YouTube Short. "
        f"Tone: {tone}. Style: {visual_style}. Creative seed: {creative_seed}. "
        "Use clear silhouettes, readable motion, strong first-frame composition, and no copyrighted characters."
    )
    video_prompt = (
        f"Generate a vertical cinematic video using Seedance 2.0. Aspect ratio 720:1280. "
        f"Duration target: {min(max(duration, 15), 45)} seconds as a Shorts sequence or shorter generated segments. "
        f"Scene direction: {creative_seed}. Camera: fast hook, smooth reveal, dynamic motion, clear payoff. "
        "Avoid real-person impersonation, graphic harm, brand logos, and unsafe instructions."
    )

    title_options = [
        f"Top Comment Built {title_subject}",
        f"The Audience Chose {title_subject}",
        "I Let The Top Comment Direct The AI",
    ]

    return ShortPackage(
        episode_id=episode_id,
        hook=hook,
        script=script,
        voiceover=script,
        visual_prompt=visual_prompt,
        video_prompt=video_prompt,
        caption_text=f"Top comment decides the next build. {next_cta}",
        title_options=title_options,
        description=(
            "The audience chose the next direction, and Top Comment Studio turned it into a safe "
            "Runway-ready Shorts production package."
        ),
        pinned_comment=next_cta,
        next_cta=next_cta,
        thumbnail_idea=f"A bold vertical frame showing the AI reveal for: {title_subject}",
        safety_notes=f"Guardrail status: {guardrail.status}. {guardrail.reason}",
        workflow_model_stack=WorkflowModelStack(workflow_registry_url=settings.runway_workflow_registry_url),
    )


def _compact_subject(comment: str) -> str:
    words = " ".join(comment.strip().split())
    if not words:
        return "The Next Episode"
    return words[:64].rstrip(" ,.;:!?-")
