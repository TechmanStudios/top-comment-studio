from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from ..settings import Settings


NANO_BANANA_PRO_MODEL = "gemini_image3_pro"
NANO_BANANA_FAST_MODEL = "gemini_2.5_flash"
NANO_BANANA_PRO_HIGH_RES_PORTRAIT_RATIO = "1536:2752"
NANO_BANANA_PRO_MAX_PORTRAIT_RATIO = "3072:5504"
GEN45_VIDEO_MODEL = "gen4.5"
VEO31_VIDEO_MODEL = "veo3.1"
RUNWAY_VERTICAL_VIDEO_RATIO = "720:1280"
GEN45_CINEMATIC_DURATION_SECONDS = 5
VEO31_FINAL_VIDEO_DURATION_SECONDS = 10
SOUND_EFFECT_MODEL = "eleven_text_to_sound_v2"
SOUND_EFFECT_REFERENCE_DURATION_SECONDS = 4.0


@dataclass(frozen=True)
class RunwayClientConfig:
    base_url: str
    api_version: str
    has_secret: bool


class RunwayClientError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        response_body: str = "",
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


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

    def list_workflows(self) -> dict[str, Any]:
        return self._request_json("GET", "/v1/workflows")

    def retrieve_workflow(self, workflow_id: str) -> dict[str, Any]:
        return self._request_json("GET", f"/v1/workflows/{workflow_id}")

    def run_workflow(
        self,
        workflow_id: str,
        node_outputs: dict[str, dict[str, dict[str, Any]]],
    ) -> dict[str, Any]:
        return self._request_json(
            "POST",
            f"/v1/workflows/{workflow_id}",
            json_body={"nodeOutputs": node_outputs},
        )

    def retrieve_workflow_invocation(self, invocation_id: str) -> dict[str, Any]:
        return self._request_json("GET", f"/v1/workflow_invocations/{invocation_id}")

    def create_text_to_image_task(
        self,
        prompt_text: str,
        *,
        model: str = NANO_BANANA_PRO_MODEL,
        ratio: str = NANO_BANANA_PRO_HIGH_RES_PORTRAIT_RATIO,
        reference_images: list[dict[str, str]] | None = None,
        seed: int | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "promptText": prompt_text,
            "ratio": ratio,
        }
        if reference_images:
            payload["referenceImages"] = reference_images
        if seed is not None:
            payload["seed"] = seed
        return self._request_json("POST", "/v1/text_to_image", json_body=payload)

    def create_image_to_video_task(
        self,
        prompt_text: str,
        prompt_image_uri: str,
        *,
        model: str = GEN45_VIDEO_MODEL,
        ratio: str = RUNWAY_VERTICAL_VIDEO_RATIO,
        duration: int = GEN45_CINEMATIC_DURATION_SECONDS,
        seed: int | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "promptText": prompt_text,
            "promptImage": [{"uri": prompt_image_uri, "position": "first"}],
            "ratio": ratio,
            "duration": duration,
        }
        if seed is not None:
            payload["seed"] = seed
        return self._request_json("POST", "/v1/image_to_video", json_body=payload)

    def create_text_to_video_task(
        self,
        prompt_text: str,
        *,
        model: str = VEO31_VIDEO_MODEL,
        ratio: str = RUNWAY_VERTICAL_VIDEO_RATIO,
        duration: int = VEO31_FINAL_VIDEO_DURATION_SECONDS,
        seed: int | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "promptText": prompt_text,
            "ratio": ratio,
            "duration": duration,
        }
        if seed is not None:
            payload["seed"] = seed
        return self._request_json("POST", "/v1/text_to_video", json_body=payload)

    def create_sound_effect_task(
        self,
        prompt_text: str,
        *,
        duration: float = SOUND_EFFECT_REFERENCE_DURATION_SECONDS,
        loop: bool = False,
    ) -> dict[str, Any]:
        return self._request_json(
            "POST",
            "/v1/sound_effect",
            json_body={
                "model": SOUND_EFFECT_MODEL,
                "promptText": prompt_text,
                "duration": duration,
                "loop": loop,
            },
        )

    def create_ephemeral_upload(self, filename: str) -> dict[str, Any]:
        return self._request_json(
            "POST",
            "/v1/uploads",
            json_body={"filename": filename, "type": "ephemeral"},
        )

    def upload_ephemeral_file(self, file_path: str | Path) -> str:
        path = Path(file_path)
        upload = self.create_ephemeral_upload(path.name)
        upload_url = str(upload.get("uploadUrl", ""))
        runway_uri = str(upload.get("runwayUri", ""))
        fields = upload.get("fields", {})
        if not upload_url or not runway_uri or not isinstance(fields, dict):
            raise RunwayClientError("Runway did not return a valid ephemeral upload target.")

        try:
            with self.new_http_client() as client:
                with path.open("rb") as file_handle:
                    response = client.post(
                        upload_url,
                        data=fields,
                        files={"file": (path.name, file_handle)},
                    )
        except OSError as exc:
            raise RunwayClientError(f"Could not read upload file: {exc}") from exc
        except httpx.HTTPError as exc:
            raise RunwayClientError(f"Runway upload request failed: {exc}") from exc

        if response.is_error:
            raise RunwayClientError(
                "Runway ephemeral upload failed.",
                status_code=response.status_code,
                response_body=response.text,
            )
        return runway_uri

    def retrieve_task(self, task_id: str) -> dict[str, Any]:
        return self._request_json("GET", f"/v1/tasks/{task_id}")

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        api_secret = self.settings.runway_api_secret
        if not api_secret:
            raise RunwayClientError(
                "RUNWAYML_HACKATHON_API_SECRET or RUNWAYML_API_SECRET is not configured."
            )

        try:
            with self.new_http_client() as client:
                response = client.request(
                    method,
                    path,
                    headers=self.build_headers(api_secret),
                    json=json_body,
                )
        except httpx.HTTPError as exc:
            raise RunwayClientError(f"Runway API request failed: {exc}") from exc

        if response.is_error:
            message = _friendly_error_message(response.status_code)
            raise RunwayClientError(
                message,
                status_code=response.status_code,
                response_body=response.text,
            )

        if not response.content:
            return {}
        return response.json()


def _friendly_error_message(status_code: int) -> str:
    if status_code in {401, 403}:
        return "Runway rejected the request. Check the API secret and account access."
    if status_code == 404:
        return "Runway could not find that workflow or invocation."
    if status_code == 429:
        return "Runway rate limited the request. Try again after a short pause."
    return f"Runway API returned HTTP {status_code}."
