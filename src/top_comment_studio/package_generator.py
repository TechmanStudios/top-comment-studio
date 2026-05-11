from .schemas import (
    AudioVisualDirectorPacket,
    CommentInput,
    GuardrailReview,
    ShortPackage,
    WorkflowModelStack,
)
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
    av_packet = build_audio_visual_director_packet(comment_input, guardrail, title_subject)
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
        f"Create a nine-image Gen/Veo reference board for a {duration}-second vertical YouTube Short. "
        f"Tone: {tone}. Style: {visual_style}. Audience signal: {av_packet.audience_signal}. "
        f"Opening visual anchor: {av_packet.visual_anchor}. Subject continuity: {av_packet.subject_focus}. "
        f"World: {av_packet.scene_world}. Motion path: {av_packet.motion_arc}. "
        "Use clear silhouettes, readable cause-and-effect motion, strong first-frame composition, and no copyrighted characters."
    )
    video_prompt = (
        "Generate one vertical cinematic audio-video scene from a unified Gen/Veo director packet. "
        "Use Gen-4.5 for silent movie-shot studies and Veo 3.1 for the final native-audio video. Aspect ratio 1080:1920. "
        f"Duration target: {min(max(duration, 15), 45)} seconds as a Shorts sequence or shorter generated segments. "
        f"Intent: {av_packet.creator_intent}. Camera: {av_packet.camera_language}. "
        f"Motion: {av_packet.motion_arc}. Audio: {av_packet.audio_design}. "
        f"Sync: {av_packet.audio_visual_sync}. Constraints: {av_packet.negative_constraints}."
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
        av_director_packet=av_packet,
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
        workflow_model_stack=WorkflowModelStack(
            workflow_registry_url=settings.runway_workflow_registry_url
        ),
    )


def build_audio_visual_director_packet(
    comment_input: CommentInput,
    guardrail: GuardrailReview,
    title_subject: str,
) -> AudioVisualDirectorPacket:
    creative_seed = guardrail.safe_interpretation
    creator_notes = _fallback(
        comment_input.creative_notes,
        "Keep the audience choice visible in the first read and preserve Bryan's approval loop.",
    )
    subject_focus = _fallback(
        comment_input.subject_focus,
        f"A safe original subject based on '{title_subject}', with one recognizable silhouette from first frame to payoff.",
    )
    scene_world = _fallback(
        comment_input.scene_world,
        f"A fictional, platform-safe world that makes this idea visual: {creative_seed}.",
    )
    motion_arc = _fallback(
        comment_input.motion_direction,
        "Start with an instantly readable hook, build through one physical transformation, and end on a clear payoff pose.",
    )
    camera_language = _fallback(
        comment_input.camera_direction,
        "Vertical cinematic push-in, clean parallax, motivated reveal, stable subject tracking, no chaotic cutting.",
    )
    audio_design = _fallback(
        comment_input.audio_direction,
        "Native Veo audio: evolving ambience, tactile motion details, one transformation accent, and a satisfying payoff hit.",
    )
    negative_constraints = _fallback(
        comment_input.quality_constraints,
        "No captions, no logos, no copyrighted characters, no real-person likeness, no graphic harm, no unsafe instructions.",
    )

    return AudioVisualDirectorPacket(
        audience_signal=comment_input.selected_comment,
        creator_intent=f"{creative_seed} Creator notes: {creator_notes}",
        subject_focus=subject_focus,
        scene_world=scene_world,
        visual_anchor=(
            "A bold 9:16 opening frame where the audience-requested subject is readable within one second."
        ),
        motion_arc=motion_arc,
        camera_language=camera_language,
        audio_design=audio_design,
        audio_visual_sync=(
            "Lock sound events to visible causes: ambience follows the world, motion sounds follow contact, "
            "the transformation accent lands on the main visual change, and the final hit lands on the payoff frame."
        ),
        negative_constraints=negative_constraints,
    )


def _compact_subject(comment: str) -> str:
    words = " ".join(comment.strip().split())
    if not words:
        return "The Next Episode"
    return words[:64].rstrip(" ,.;:!?-")


def _fallback(value: str, fallback: str) -> str:
    normalized = " ".join(value.split())
    return normalized or fallback
