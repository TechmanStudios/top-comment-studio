import json

import httpx
import top_comment_studio.app as app_module
from fastapi.testclient import TestClient

from top_comment_studio.app import (
    advance_direct_generation,
    advance_image_board_generation,
    build_direct_image_prompt,
    build_direct_gen45_prompt,
    build_veo31_final_video_prompt,
    create_episode_record,
    direct_generation_blockers,
    extract_failure,
    extract_progress,
    image_board_submission_blockers,
    image_board_video_submission_blockers,
    rendered_video_urls,
    summarize_asset_counts,
    submit_record_to_runway,
)
from top_comment_studio.runway.client import RunwayClient
from top_comment_studio.runway.workflows import (
    REQUIRED_WORKFLOW_INPUTS,
    build_workflow_preview,
    clamp_runway_video_duration,
    workflow_submission_blockers,
)
from top_comment_studio.schemas import (
    CommentInput,
    RunwayDirectGenerationState,
    RunwayImageBoardRowState,
    RunwayImageBoardState,
    RunwayWorkflowState,
)
from top_comment_studio.settings import Settings
from top_comment_studio.storage import ChainStore


def test_builds_runway_workflow_preview_with_node_outputs():
    record = create_episode_record(
        CommentInput(
            selected_comment="Make the AI build a floating city powered by storms.",
            previous_video_summary="The audience asked what should power the city.",
            previous_video_cta="What powers it next?",
            creative_notes="Make the reveal feel huge but safe.",
            target_duration_seconds=60,
        )
    )
    settings = Settings(
        runway_workflow_id="workflow-123",
        runway_workflow_node_map_json=_node_map_json(),
    )

    preview = build_workflow_preview(record, settings)

    assert preview.can_submit is True
    assert preview.duration_seconds == 4
    assert preview.aspect_ratio == "1080:1920"
    assert preview.node_outputs["node-episode_id"]["prompt"]["value"] == record.episode_id
    assert "floating city" in preview.node_outputs["node-audience_signal"]["prompt"]["value"]
    assert "audio_design" in preview.node_outputs["node-av_director_packet"]["prompt"]["value"]
    assert "transformation accent" in preview.node_outputs["node-audio_prompt"]["prompt"]["value"]
    assert preview.node_outputs["node-duration_seconds"]["prompt"]["value"] == "4"


def test_runway_video_duration_is_clamped_to_supported_range():
    assert clamp_runway_video_duration(1) == 2
    assert clamp_runway_video_duration(8) == 8
    assert clamp_runway_video_duration(60) == 10


def test_submission_blockers_require_approval_secret_and_config():
    record = create_episode_record(
        CommentInput(selected_comment="Build a storm-powered sky bridge.")
    )
    preview = build_workflow_preview(
        record,
        Settings(runway_workflow_id="", runway_workflow_node_map_json="{}"),
    )

    blockers = workflow_submission_blockers(
        record,
        preview,
        has_runway_secret=False,
        creator_approved=False,
    )

    assert "Creator approval is required before submitting to Runway." in blockers
    assert "Set RUNWAYML_HACKATHON_API_SECRET before submitting to Runway." in blockers
    assert any("RUNWAY_WORKFLOW_ID" in blocker for blocker in blockers)


def test_submit_record_to_runway_starts_configured_workflow(monkeypatch):
    monkeypatch.setenv("RUNWAYML_HACKATHON_API_SECRET", "test-secret")
    monkeypatch.setattr(
        app_module,
        "settings",
        Settings(
            runway_workflow_id="workflow-123",
            runway_workflow_node_map_json=_node_map_json(),
        ),
    )
    record = create_episode_record(
        CommentInput(selected_comment="Make the AI build a floating city powered by storms.")
    )
    client = FakeWorkflowRunwayClient()

    updated, message, error = submit_record_to_runway(
        record,
        creator_approved=True,
        client=client,
    )

    assert error == ""
    assert message == "Submitted to Runway invocation invocation-123."
    assert updated.runway.workflow_id == "workflow-123"
    assert updated.runway.invocation_id == "invocation-123"
    assert updated.runway.status == "submitted"
    assert client.workflow_requests[0]["workflow_id"] == "workflow-123"
    assert set(client.workflow_requests[0]["node_outputs"]) == {
        f"node-{name}" for name in REQUIRED_WORKFLOW_INPUTS
    }


def test_rendered_video_urls_prefers_workflow_output():
    record = create_episode_record(
        CommentInput(selected_comment="Make the AI build a floating city powered by storms.")
    )
    record.runway_direct = RunwayDirectGenerationState(
        output_urls=["https://example.com/direct.mp4"]
    )
    record.runway_image_board = RunwayImageBoardState(
        video_output_urls=["https://example.com/board.mp4"]
    )
    record.runway = RunwayWorkflowState(output_urls=["https://example.com/v66.mp4"])

    assert rendered_video_urls(record) == ["https://example.com/v66.mp4"]

    record.runway = RunwayWorkflowState()

    assert rendered_video_urls(record) == ["https://example.com/board.mp4"]


def test_package_page_is_render_focused(monkeypatch, tmp_path):
    monkeypatch.setattr(
        app_module,
        "settings",
        Settings(
            data_dir=tmp_path,
            runway_workflow_id="workflow-123",
            runway_workflow_node_map_json=_node_map_json(),
        ),
    )
    record = create_episode_record(
        CommentInput(selected_comment="Make the AI build a floating city powered by storms.")
    )
    ChainStore(tmp_path).save(record)

    response = TestClient(app_module.app).get(f"/package/{record.episode_id}")

    assert response.status_code == 200
    assert "Render output" in response.text
    assert "Start render" not in response.text
    assert "Creator-approved for v66 Runway generation" not in response.text
    assert "Shorts package" not in response.text
    assert "Runway workflow handoff" not in response.text
    assert "Nine-image reference board" not in response.text


def test_homepage_never_shows_saved_render_panel(monkeypatch, tmp_path):
    monkeypatch.setattr(
        app_module,
        "settings",
        Settings(
            data_dir=tmp_path,
            runway_workflow_id="workflow-123",
            runway_workflow_node_map_json=_node_map_json(),
        ),
    )
    record = create_episode_record(
        CommentInput(selected_comment="Make the AI build a floating city powered by storms.")
    )
    record.runway = RunwayWorkflowState(
        invocation_id="invocation-123",
        status="failed",
        failure="Succeeded without exposed workflow outputs.",
        output_urls=["https://example.com/stale.mp4"],
    )
    ChainStore(tmp_path).save(record)

    response = TestClient(app_module.app).get("/")

    assert response.status_code == 200
    assert "Render output" not in response.text
    assert "Render blocked" not in response.text
    assert "View rendered content" not in response.text
    assert "Refresh render" not in response.text
    assert "stale.mp4" not in response.text


def test_homepage_has_ready_demo_signal_and_collapsed_controls(monkeypatch, tmp_path):
    monkeypatch.setattr(
        app_module,
        "settings",
        Settings(
            data_dir=tmp_path,
            runway_workflow_id="workflow-123",
            runway_workflow_node_map_json=_node_map_json(),
        ),
    )

    response = TestClient(app_module.app).get("/")

    assert response.status_code == 200
    assert "storm-powered city forming in the clouds" in response.text
    assert "Try a real audience comment" in response.text
    assert "Usual render time: about 7-8 minutes." in response.text
    assert "Director controls" in response.text
    assert "Hackathon demo view only" in response.text
    assert 'name="target_tone" value="curious, cinematic, participatory" readonly' in response.text
    assert "Duration seconds" not in response.text


def test_create_package_route_starts_render_without_second_approval(monkeypatch, tmp_path):
    monkeypatch.setenv("RUNWAYML_HACKATHON_API_SECRET", "test-secret")
    monkeypatch.setattr(
        app_module,
        "settings",
        Settings(
            data_dir=tmp_path,
            runway_workflow_id="workflow-123",
            runway_workflow_node_map_json=_node_map_json(),
        ),
    )

    class RouteWorkflowClient(FakeWorkflowRunwayClient):
        instances: list["RouteWorkflowClient"] = []

        def __init__(self, settings: Settings) -> None:
            super().__init__()
            self.settings = settings
            self.instances.append(self)

    monkeypatch.setattr(app_module, "RunwayClient", RouteWorkflowClient)

    response = TestClient(app_module.app).post(
        "/package",
        data={
            "selected_comment": "Make the video a city powered by storms.",
            "target_tone": "chaotic test override",
            "visual_style": "unstable test style",
            "creative_notes": "force a custom post-generation branch",
            "subject_focus": "change the subject every shot",
            "scene_world": "break the proven world defaults",
            "motion_direction": "use a disruptive motion test",
            "camera_direction": "use a disruptive camera test",
            "audio_direction": "use a disruptive audio test",
            "quality_constraints": "ignore normal constraints",
        },
    )
    record = ChainStore(tmp_path).latest()

    assert response.status_code == 200
    assert record is not None
    assert record.runway.invocation_id == "invocation-123"
    assert "Rendering" in response.text
    assert "Start render" not in response.text
    assert "Creator-approved for v66 Runway generation" not in response.text
    assert RouteWorkflowClient.instances[0].workflow_requests[0]["workflow_id"] == "workflow-123"
    assert record.production_context.creative_notes == ""
    assert record.production_context.target_tone == "curious, cinematic, participatory"
    assert record.production_context.visual_style == "vertical cinematic YouTube Short"
    packet_json = RouteWorkflowClient.instances[0].workflow_requests[0]["node_outputs"][
        "node-av_director_packet"
    ]["prompt"]["value"]
    assert "custom post-generation branch" not in packet_json
    assert "disruptive audio test" not in packet_json


def test_runway_status_waits_for_succeeded_output_propagation(monkeypatch, tmp_path):
    monkeypatch.setenv("RUNWAYML_HACKATHON_API_SECRET", "test-secret")
    monkeypatch.setattr(
        app_module,
        "settings",
        Settings(
            data_dir=tmp_path,
            runway_workflow_id="workflow-123",
            runway_workflow_node_map_json=_node_map_json(),
        ),
    )

    record = create_episode_record(
        CommentInput(selected_comment="Make the AI build a floating city powered by storms.")
    )
    record.runway = RunwayWorkflowState(
        workflow_id="workflow-123",
        invocation_id="invocation-123",
        status="submitted",
        submitted_at=app_module.current_timestamp(),
    )
    ChainStore(tmp_path).save(record)

    class PropagatingWorkflowClient:
        def __init__(self, settings: Settings) -> None:
            self.settings = settings

        def retrieve_workflow_invocation(self, invocation_id: str) -> dict[str, object]:
            assert invocation_id == "invocation-123"
            return {"id": invocation_id, "status": "SUCCEEDED", "output": {}}

    monkeypatch.setattr(app_module, "RunwayClient", PropagatingWorkflowClient)

    response = TestClient(app_module.app).get(f"/package/{record.episode_id}/runway-status")
    updated = ChainStore(tmp_path).get(record.episode_id)

    assert response.status_code == 200
    assert "Rendering" in response.text
    assert "Render blocked" not in response.text
    assert "without exposed workflow outputs" not in response.text
    assert updated is not None
    assert updated.runway.status == "processing"
    assert updated.runway.progress == app_module.WORKFLOW_OUTPUT_PROPAGATION_PROGRESS
    assert updated.runway.failure == ""


def test_direct_generation_blockers_require_approval_secret_and_safe_comment():
    record = create_episode_record(
        CommentInput(selected_comment="Build a storm-powered sky bridge.")
    )
    record.guardrail.status = "rejected"

    blockers = direct_generation_blockers(
        record,
        has_runway_secret=False,
        creator_approved=False,
    )

    assert "Creator approval is required before submitting direct Runway generation." in blockers
    assert "Set RUNWAYML_HACKATHON_API_SECRET before submitting to Runway." in blockers
    assert "Rejected comments cannot be submitted to Runway." in blockers


def test_builds_direct_generation_prompts_within_runway_limits():
    record = create_episode_record(
        CommentInput(
            selected_comment="Make the AI build a floating city powered by storms.",
            creative_notes="Make the opening frame readable on mobile.",
            audio_direction="Storm hum, wind detail, and a clean reveal hit.",
        )
    )

    image_prompt = build_direct_image_prompt(record)
    gen45_prompt = build_direct_gen45_prompt(record)

    assert len(image_prompt) <= 950
    assert len(gen45_prompt) <= 950
    assert "no text overlays" in image_prompt.lower()
    assert "Gen-4.5" in gen45_prompt
    assert "supplied first frame" in gen45_prompt
    assert "unified audio-video director packet" in gen45_prompt


def test_builds_veo31_final_video_prompt_within_runway_limits():
    record = create_episode_record(
        CommentInput(
            selected_comment="Make the AI build a floating city powered by storms.",
            creative_notes="Use the nine refs as continuity anchors.",
            audio_direction="Thunder bed, turbine whine, rain texture, and a soft payoff hit.",
        )
    )

    prompt = build_veo31_final_video_prompt(record)

    assert len(prompt) <= 950
    assert "Veo 3.1" in prompt
    assert "nine-image board" in prompt
    assert "native audio" in prompt
    assert "Audio-video sync" in prompt


def test_image_board_submission_blockers_require_approval_secret_and_config(monkeypatch):
    monkeypatch.setattr(
        app_module,
        "settings",
        Settings(
            runway_workflow_node_map_json="{}",
            runway_image_board_row_1_workflow_id="",
            runway_image_board_row_2_workflow_id="",
            runway_image_board_row_3_workflow_id="",
        ),
    )
    record = create_episode_record(CommentInput(selected_comment="Build a storm gate."))

    blockers = image_board_submission_blockers(
        record,
        has_runway_secret=False,
        creator_approved=False,
    )

    assert "Creator approval is required before submitting the image board." in blockers
    assert "Set RUNWAYML_HACKATHON_API_SECRET before submitting to Runway." in blockers
    assert any("RUNWAY_IMAGE_BOARD_ROW_1_WORKFLOW_ID" in blocker for blocker in blockers)


def test_image_board_video_blockers_require_nine_images():
    record = create_episode_record(CommentInput(selected_comment="Build a storm gate."))
    record.runway_image_board = RunwayImageBoardState(
        rows=[
            RunwayImageBoardRowState(
                label="row1",
                status="SUCCEEDED",
                output_urls=["https://example.com/ref-1.png"],
            )
        ]
    )

    blockers = image_board_video_submission_blockers(
        record,
        has_runway_secret=True,
        creator_approved=True,
    )

    assert any(
        "Generate and refresh all nine image-board outputs" in blocker for blocker in blockers
    )


def test_settings_prefers_hackathon_runway_secret(monkeypatch):
    monkeypatch.setenv("RUNWAYML_API_SECRET", "standard-secret")
    monkeypatch.setenv("RUNWAYML_HACKATHON_API_SECRET", "hackathon-secret")

    settings = Settings()

    assert settings.runway_api_secret == "hackathon-secret"
    assert settings.has_runway_secret is True


def test_extract_failure_surfaces_workflow_node_errors():
    failure = extract_failure(
        {
            "status": "RUNNING",
            "nodeErrors": {
                "node-123": {
                    "nodeName": "Combine 06: duration + aspect",
                    "message": "Invalid task options: strings.0: expected string",
                }
            },
        }
    )

    assert "Combine 06: duration + aspect" in failure
    assert "expected string" in failure


def test_extract_progress_clamps_runway_progress_value():
    assert extract_progress({"progress": 0.8913043478260869}) == 0.8913043478260869
    assert extract_progress({"progress": 2}) == 1.0
    assert extract_progress({"progress": -1}) == 0.0
    assert extract_progress({"progress": "almost"}) is None


def test_summarize_asset_counts_groups_media_urls():
    counts = summarize_asset_counts(
        [
            "https://example.com/final.mp4?token=secret",
            "https://example.com/cue.mp3?token=secret",
            "https://example.com/ref.png",
            "https://example.com/artifact.bin",
        ]
    )

    assert counts == {"video": 1, "audio": 1, "image": 1, "other": 1}


def test_extract_failure_surfaces_missing_published_outputs():
    failure = extract_failure({"status": "SUCCEEDED", "output": {}})

    assert "without exposed workflow outputs" in failure
    assert "every upstream node" in failure


def test_extract_failure_prefers_node_errors_before_missing_outputs():
    failure = extract_failure(
        {
            "status": "SUCCEEDED",
            "output": {},
            "nodeErrors": {
                "image-node": {
                    "nodeName": "Ref Image 01",
                    "message": "No model variant mapping for app node type: gpt-tidepool-alpha",
                }
            },
        }
    )

    assert "Ref Image 01" in failure
    assert "gemini_image3_pro" in failure


def test_extract_failure_guides_gpt_image_variant_mapping():
    failure = extract_failure(
        {
            "status": "SUCCEEDED",
            "output": {"audio-node": ["https://example.com/audio.mp3"]},
            "nodeErrors": {
                "image-node": {
                    "nodeName": "Ref Image 01",
                    "message": "No model variant mapping for app node type: gpt-tidepool-alpha",
                }
            },
        }
    )

    assert "Ref Image 01" in failure
    assert "gemini_image3_pro" in failure


def test_runway_client_starts_nano_banana_image_task_with_mocked_http(monkeypatch):
    monkeypatch.delenv("RUNWAYML_HACKATHON_API_SECRET", raising=False)
    monkeypatch.setenv("RUNWAYML_API_SECRET", "test-secret")
    request_bodies = []

    def handler(request: httpx.Request) -> httpx.Response:
        request_bodies.append(json.loads(request.content.decode("utf-8")))
        assert request.url.path == "/v1/text_to_image"
        assert request.headers["Authorization"] == "Bearer test-secret"
        assert request.headers["X-Runway-Version"] == "2024-11-06"
        return httpx.Response(200, json={"id": "task-123"})

    transport = httpx.MockTransport(handler)
    client = RunwayClient(Settings(runway_api_base_url="https://api.dev.runwayml.com"))

    def new_http_client() -> httpx.Client:
        return httpx.Client(base_url=client.settings.runway_api_base_url, transport=transport)

    monkeypatch.setattr(client, "new_http_client", new_http_client)

    response = client.create_text_to_image_task(
        "A safe fictional storm-powered floating city, vertical cinematic frame.",
        reference_images=[{"uri": "https://example.com/ref.png", "tag": "city_ref"}],
        seed=123,
    )

    assert response == {"id": "task-123"}
    assert request_bodies == [
        {
            "model": "gemini_image3_pro",
            "promptText": "A safe fictional storm-powered floating city, vertical cinematic frame.",
            "ratio": "1536:2752",
            "referenceImages": [{"uri": "https://example.com/ref.png", "tag": "city_ref"}],
            "seed": 123,
        }
    ]


def test_runway_client_starts_gen45_image_to_video_task_with_mocked_http(monkeypatch):
    monkeypatch.delenv("RUNWAYML_HACKATHON_API_SECRET", raising=False)
    monkeypatch.setenv("RUNWAYML_API_SECRET", "test-secret")
    request_bodies = []

    def handler(request: httpx.Request) -> httpx.Response:
        request_bodies.append(json.loads(request.content.decode("utf-8")))
        assert request.url.path == "/v1/image_to_video"
        assert request.headers["Authorization"] == "Bearer test-secret"
        assert request.headers["X-Runway-Version"] == "2024-11-06"
        return httpx.Response(200, json={"id": "video-task-123"})

    transport = httpx.MockTransport(handler)
    client = RunwayClient(Settings(runway_api_base_url="https://api.dev.runwayml.com"))

    def new_http_client() -> httpx.Client:
        return httpx.Client(base_url=client.settings.runway_api_base_url, transport=transport)

    monkeypatch.setattr(client, "new_http_client", new_http_client)

    response = client.create_image_to_video_task(
        "Camera slowly pushes into the storm-powered floating city.",
        "https://example.com/nano-banana-pro.png",
        seed=456,
    )

    assert response == {"id": "video-task-123"}
    assert request_bodies == [
        {
            "model": "gen4.5",
            "promptText": "Camera slowly pushes into the storm-powered floating city.",
            "promptImage": [
                {"uri": "https://example.com/nano-banana-pro.png", "position": "first"}
            ],
            "ratio": "720:1280",
            "duration": 5,
            "seed": 456,
        }
    ]


def test_runway_client_starts_veo31_text_to_video_task_with_mocked_http(monkeypatch):
    monkeypatch.delenv("RUNWAYML_HACKATHON_API_SECRET", raising=False)
    monkeypatch.setenv("RUNWAYML_API_SECRET", "test-secret")
    request_bodies = []

    def handler(request: httpx.Request) -> httpx.Response:
        request_bodies.append(json.loads(request.content.decode("utf-8")))
        assert request.url.path == "/v1/text_to_video"
        assert request.headers["Authorization"] == "Bearer test-secret"
        assert request.headers["X-Runway-Version"] == "2024-11-06"
        return httpx.Response(200, json={"id": "video-task-refs"})

    transport = httpx.MockTransport(handler)
    client = RunwayClient(Settings(runway_api_base_url="https://api.dev.runwayml.com"))

    def new_http_client() -> httpx.Client:
        return httpx.Client(base_url=client.settings.runway_api_base_url, transport=transport)

    monkeypatch.setattr(client, "new_http_client", new_http_client)

    response = client.create_text_to_video_task(
        "The city rises through storm clouds.",
        duration=10,
        seed=789,
    )

    assert response == {"id": "video-task-refs"}
    assert request_bodies == [
        {
            "model": "veo3.1",
            "promptText": "The city rises through storm clouds.",
            "ratio": "720:1280",
            "duration": 10,
            "seed": 789,
        }
    ]


def test_runway_client_starts_sound_effect_task_with_mocked_http(monkeypatch):
    monkeypatch.delenv("RUNWAYML_HACKATHON_API_SECRET", raising=False)
    monkeypatch.setenv("RUNWAYML_API_SECRET", "test-secret")
    request_bodies = []

    def handler(request: httpx.Request) -> httpx.Response:
        request_bodies.append(json.loads(request.content.decode("utf-8")))
        assert request.url.path == "/v1/sound_effect"
        assert request.headers["Authorization"] == "Bearer test-secret"
        assert request.headers["X-Runway-Version"] == "2024-11-06"
        return httpx.Response(200, json={"id": "audio-task-123"})

    transport = httpx.MockTransport(handler)
    client = RunwayClient(Settings(runway_api_base_url="https://api.dev.runwayml.com"))

    def new_http_client() -> httpx.Client:
        return httpx.Client(base_url=client.settings.runway_api_base_url, transport=transport)

    monkeypatch.setattr(client, "new_http_client", new_http_client)

    response = client.create_sound_effect_task(
        "Deep storm ambience, distant thunder, clean cinematic low-end rumble.",
        loop=True,
    )

    assert response == {"id": "audio-task-123"}
    assert request_bodies == [
        {
            "model": "eleven_text_to_sound_v2",
            "promptText": "Deep storm ambience, distant thunder, clean cinematic low-end rumble.",
            "duration": 4.0,
            "loop": True,
        }
    ]


def test_runway_client_uploads_ephemeral_file_with_mocked_http(monkeypatch, tmp_path):
    monkeypatch.delenv("RUNWAYML_HACKATHON_API_SECRET", raising=False)
    monkeypatch.setenv("RUNWAYML_API_SECRET", "test-secret")
    upload_file = tmp_path / "reference.png"
    upload_file.write_bytes(b"fake-image-bytes" * 80)
    seen_requests: list[tuple[str, str, bytes]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = request.read()
        seen_requests.append((request.method, request.url.host, body))
        if request.url.host == "api.dev.runwayml.com":
            assert request.url.path == "/v1/uploads"
            assert request.headers["Authorization"] == "Bearer test-secret"
            assert json.loads(body.decode("utf-8")) == {
                "filename": "reference.png",
                "type": "ephemeral",
            }
            return httpx.Response(
                200,
                json={
                    "uploadUrl": "https://uploads.example.com/runway-upload",
                    "fields": {"key": "uploads/reference.png", "policy": "signed-policy"},
                    "runwayUri": "runway://ephemeral/reference.png",
                },
            )
        assert request.url.host == "uploads.example.com"
        assert request.url.path == "/runway-upload"
        assert b"signed-policy" in body
        assert b"fake-image-bytes" in body
        return httpx.Response(204)

    transport = httpx.MockTransport(handler)
    client = RunwayClient(Settings(runway_api_base_url="https://api.dev.runwayml.com"))

    def new_http_client() -> httpx.Client:
        return httpx.Client(base_url=client.settings.runway_api_base_url, transport=transport)

    monkeypatch.setattr(client, "new_http_client", new_http_client)

    runway_uri = client.upload_ephemeral_file(upload_file)

    assert runway_uri == "runway://ephemeral/reference.png"
    assert [(method, host) for method, host, _ in seen_requests] == [
        ("POST", "api.dev.runwayml.com"),
        ("POST", "uploads.example.com"),
    ]


def test_advance_direct_generation_submits_gen45_after_image_succeeds():
    record = create_episode_record(
        CommentInput(selected_comment="Make the AI build a floating city powered by storms.")
    )
    record.runway_direct = RunwayDirectGenerationState(image_task_id="image-task-123")
    client = FakeDirectRunwayClient()

    updated = advance_direct_generation(record, client, "2026-05-09T00:00:00+00:00")

    assert updated.runway_direct.status == "video_submitted"
    assert updated.runway_direct.video_task_id == "video-task-123"
    assert updated.runway_direct.image_output_urls == ["https://example.com/image.png"]
    assert client.video_requests == [
        {
            "prompt_image_uri": "https://example.com/image.png",
            "model": "gen4.5",
            "ratio": "720:1280",
            "duration": 5,
        }
    ]


def test_advance_direct_generation_collects_gen45_output():
    record = create_episode_record(
        CommentInput(selected_comment="Make the AI build a floating city powered by storms.")
    )
    record.runway_direct = RunwayDirectGenerationState(video_task_id="video-task-123")
    client = FakeDirectRunwayClient()

    updated = advance_direct_generation(record, client, "2026-05-09T00:00:00+00:00")

    assert updated.runway_direct.status == "SUCCEEDED"
    assert updated.runway_direct.output_urls == ["https://example.com/video.mp4"]
    assert updated.runway_direct.failure == ""


def test_advance_image_board_generation_collects_rows_and_video():
    record = create_episode_record(
        CommentInput(selected_comment="Make the AI build a floating city powered by storms.")
    )
    record.runway_image_board = RunwayImageBoardState(
        rows=[
            RunwayImageBoardRowState(
                label="row1",
                workflow_id="workflow-row1",
                invocation_id="board-row-1",
            )
        ],
        video_task_id="video-task-refs",
        video_status="video_submitted",
    )
    client = FakeImageBoardRunwayClient()

    updated = advance_image_board_generation(record, client, "2026-05-09T00:00:00+00:00")

    assert updated.runway_image_board.status == "images_ready"
    assert updated.runway_image_board.rows[0].status == "SUCCEEDED"
    assert updated.runway_image_board.rows[0].output_urls == [
        "https://example.com/ref-1.png",
        "https://example.com/ref-2.png",
        "https://example.com/ref-3.png",
    ]
    assert updated.runway_image_board.video_status == "SUCCEEDED"
    assert updated.runway_image_board.video_output_urls == ["https://example.com/final.mp4"]


def test_runway_client_retrieves_task_with_mocked_http(monkeypatch):
    monkeypatch.delenv("RUNWAYML_HACKATHON_API_SECRET", raising=False)
    monkeypatch.setenv("RUNWAYML_API_SECRET", "test-secret")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/tasks/task-123"
        return httpx.Response(200, json={"id": "task-123", "status": "SUCCEEDED"})

    transport = httpx.MockTransport(handler)
    client = RunwayClient(Settings(runway_api_base_url="https://api.dev.runwayml.com"))

    def new_http_client() -> httpx.Client:
        return httpx.Client(base_url=client.settings.runway_api_base_url, transport=transport)

    monkeypatch.setattr(client, "new_http_client", new_http_client)

    assert client.retrieve_task("task-123") == {"id": "task-123", "status": "SUCCEEDED"}


def test_runway_client_runs_workflow_with_mocked_http(monkeypatch):
    monkeypatch.delenv("RUNWAYML_HACKATHON_API_SECRET", raising=False)
    monkeypatch.setenv("RUNWAYML_API_SECRET", "test-secret")
    request_bodies = []

    def handler(request: httpx.Request) -> httpx.Response:
        request_bodies.append(json.loads(request.content.decode("utf-8")))
        assert request.url.path == "/v1/workflows/workflow-123"
        assert request.headers["Authorization"] == "Bearer test-secret"
        assert request.headers["X-Runway-Version"] == "2024-11-06"
        return httpx.Response(200, json={"id": "invocation-123"})

    transport = httpx.MockTransport(handler)
    client = RunwayClient(Settings(runway_api_base_url="https://api.dev.runwayml.com"))

    def new_http_client() -> httpx.Client:
        return httpx.Client(base_url=client.settings.runway_api_base_url, transport=transport)

    monkeypatch.setattr(client, "new_http_client", new_http_client)

    response = client.run_workflow(
        "workflow-123",
        {"node-prompt": {"value": {"type": "primitive", "value": "hello"}}},
    )

    assert response == {"id": "invocation-123"}
    assert request_bodies == [
        {"nodeOutputs": {"node-prompt": {"value": {"type": "primitive", "value": "hello"}}}}
    ]


def _node_map_json() -> str:
    return json.dumps({name: {"node_id": f"node-{name}"} for name in REQUIRED_WORKFLOW_INPUTS})


class FakeWorkflowRunwayClient:
    def __init__(self) -> None:
        self.workflow_requests = []

    def run_workflow(
        self,
        workflow_id: str,
        node_outputs: dict[str, dict[str, dict[str, object]]],
    ) -> dict[str, str]:
        self.workflow_requests.append(
            {
                "workflow_id": workflow_id,
                "node_outputs": node_outputs,
            }
        )
        return {"workflowInvocationId": "invocation-123"}


class FakeDirectRunwayClient:
    def __init__(self) -> None:
        self.video_requests = []

    def retrieve_task(self, task_id: str) -> dict[str, object]:
        if task_id == "image-task-123":
            return {
                "id": task_id,
                "status": "SUCCEEDED",
                "output": ["https://example.com/image.png"],
            }
        return {
            "id": task_id,
            "status": "SUCCEEDED",
            "output": ["https://example.com/video.mp4"],
        }

    def create_image_to_video_task(
        self,
        prompt_text: str,
        prompt_image_uri: str,
        *,
        model: str,
        ratio: str,
        duration: int,
    ) -> dict[str, str]:
        self.video_requests.append(
            {
                "prompt_image_uri": prompt_image_uri,
                "model": model,
                "ratio": ratio,
                "duration": duration,
            }
        )
        assert "Gen-4.5" in prompt_text
        assert "supplied first frame" in prompt_text
        assert "unified audio-video director packet" in prompt_text
        return {"id": "video-task-123"}


class FakeImageBoardRunwayClient:
    def retrieve_workflow_invocation(self, invocation_id: str) -> dict[str, object]:
        assert invocation_id == "board-row-1"
        return {
            "id": invocation_id,
            "status": "SUCCEEDED",
            "output": {
                "image-1": "https://example.com/ref-1.png",
                "image-2": "https://example.com/ref-2.png",
                "image-3": "https://example.com/ref-3.png",
            },
        }

    def retrieve_task(self, task_id: str) -> dict[str, object]:
        assert task_id == "video-task-refs"
        return {
            "id": task_id,
            "status": "SUCCEEDED",
            "output": ["https://example.com/final.mp4"],
        }
