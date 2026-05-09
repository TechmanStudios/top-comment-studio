DEFAULT_ASPECT_RATIO = "720:1280"
DEFAULT_VIDEO_MODEL = "Seedance 2.0"
DEFAULT_IMAGE_MODEL = "OpenAI Images 2.0"
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
