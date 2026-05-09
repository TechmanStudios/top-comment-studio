from dataclasses import dataclass

import httpx

from ..settings import Settings


@dataclass(frozen=True)
class RunwayClientConfig:
    base_url: str
    api_version: str
    has_secret: bool


class RunwayClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def config(self) -> RunwayClientConfig:
        return RunwayClientConfig(
            base_url=self.settings.runway_api_base_url,
            api_version=self.settings.runway_api_version,
            has_secret=self.settings.has_runway_secret,
        )

    def build_headers(self, api_secret: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {api_secret}",
            "X-Runway-Version": self.settings.runway_api_version,
            "Content-Type": "application/json",
        }

    def new_http_client(self) -> httpx.Client:
        return httpx.Client(base_url=self.settings.runway_api_base_url, timeout=60)
