from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Top Comment Studio")
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "debug")
    runway_api_base_url: str = os.getenv("RUNWAYML_API_BASE_URL", "https://api.dev.runwayml.com")
    runway_api_version: str = os.getenv("RUNWAYML_API_VERSION", "2024-11-06")
    runway_workflow_registry_url: str = os.getenv(
        "RUNWAY_WORKFLOW_REGISTRY_URL",
        "https://dev.runwayml.com/organization/8f8366b8-b7b6-4f9c-baae-f72c16c9f79f/workflows",
    )
    runway_workflow_id: str = os.getenv("RUNWAY_WORKFLOW_ID", "")
    runway_workflow_name: str = os.getenv("RUNWAY_WORKFLOW_NAME", "TCS Gen/Veo Director v2")
    runway_workflow_node_map_json: str = os.getenv("RUNWAY_WORKFLOW_NODE_MAP_JSON", "{}")
    runway_image_board_row_1_workflow_id: str = os.getenv(
        "RUNWAY_IMAGE_BOARD_ROW_1_WORKFLOW_ID", ""
    )
    runway_image_board_row_2_workflow_id: str = os.getenv(
        "RUNWAY_IMAGE_BOARD_ROW_2_WORKFLOW_ID", ""
    )
    runway_image_board_row_3_workflow_id: str = os.getenv(
        "RUNWAY_IMAGE_BOARD_ROW_3_WORKFLOW_ID", ""
    )
    data_dir: Path = Path(os.getenv("TOP_COMMENT_STUDIO_DATA_DIR", "data/local"))

    @property
    def runway_api_secret(self) -> str:
        hackathon_secret = os.getenv("RUNWAYML_HACKATHON_API_SECRET", "")
        if _is_configured_secret(hackathon_secret, "your_runway_hackathon_api_secret_here"):
            return hackathon_secret

        secret = os.getenv("RUNWAYML_API_SECRET", "")
        if _is_configured_secret(secret, "your_runway_api_secret_here"):
            return secret
        return ""

    @property
    def has_runway_secret(self) -> bool:
        return bool(self.runway_api_secret)

    @property
    def has_runway_workflow_id(self) -> bool:
        return bool(
            self.runway_workflow_id and self.runway_workflow_id != "your_published_workflow_id_here"
        )

    @property
    def runway_image_board_workflow_ids(self) -> dict[str, str]:
        return {
            "row1": self.runway_image_board_row_1_workflow_id,
            "row2": self.runway_image_board_row_2_workflow_id,
            "row3": self.runway_image_board_row_3_workflow_id,
        }

    @property
    def has_runway_image_board_workflows(self) -> bool:
        return all(
            _is_configured_secret(workflow_id, "your_published_workflow_id_here")
            for workflow_id in self.runway_image_board_workflow_ids.values()
        )


def get_settings() -> Settings:
    return Settings()


def _is_configured_secret(value: str, placeholder: str) -> bool:
    return bool(value and value != placeholder)
