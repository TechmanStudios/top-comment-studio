DEFAULT_ASPECT_RATIO = "1080:1920"
DEFAULT_VIDEO_MODEL = "Gen-4.5 shot studies + Veo 3.1 unified audio-video final"
DEFAULT_IMAGE_MODEL = "Nano Banana Pro (Gemini 3 Pro Image)"
DEFAULT_LLM_MODEL = "GPT 5.5"


def workflow_prompt_summary(video_prompt: str, visual_prompt: str) -> str:
    return "\n\n".join(
        [
            f"Video model: {DEFAULT_VIDEO_MODEL}",
            f"Image model: {DEFAULT_IMAGE_MODEL}",
            f"LLM text model: {DEFAULT_LLM_MODEL}",
            f"Aspect ratio: {DEFAULT_ASPECT_RATIO}",
            "Video prompt:",
            video_prompt,
            "Image/reference prompt:",
            visual_prompt,
        ]
    )
