from pydantic import BaseModel


class WorkflowEndpointPlan(BaseModel):
    registry_url: str
    llm_text_generation: str = "GPT 5.5"
    image_generation: str = "OpenAI Images 2.0"
    video_generation: str = "Seedance 2.0"
    preferred_video_model_id: str = "seedance2"
    preferred_image_model_id: str = "openai/gpt_image_2"
    status: str = "planned"


def describe_workflow_plan(registry_url: str) -> WorkflowEndpointPlan:
    return WorkflowEndpointPlan(registry_url=registry_url)
