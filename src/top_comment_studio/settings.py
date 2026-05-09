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
    data_dir: Path = Path(os.getenv("TOP_COMMENT_STUDIO_DATA_DIR", "data/local"))

    @property
    def has_runway_secret(self) -> bool:
        return bool(os.getenv("RUNWAYML_API_SECRET"))


def get_settings() -> Settings:
    return Settings()
