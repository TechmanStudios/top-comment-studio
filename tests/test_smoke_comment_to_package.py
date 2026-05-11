import json
from pathlib import Path

from top_comment_studio.app import create_episode_record
from top_comment_studio.schemas import CommentInput
from top_comment_studio.storage import ChainStore


def test_comment_to_package_smoke(tmp_path):
    payload = json.loads(Path("data/samples/sample_comments.json").read_text(encoding="utf-8"))[0]
    comment_input = CommentInput.model_validate(payload)

    record = create_episode_record(comment_input)
    saved_path = ChainStore(tmp_path).save(record)

    assert record.guardrail.status == "approved"
    assert (
        "Gen-4.5 shot studies + Veo 3.1 unified audio-video final"
        == record.package.workflow_model_stack.video_generation
    )
    assert (
        "Nano Banana Pro (Gemini 3 Pro Image)"
        == record.package.workflow_model_stack.image_generation
    )
    assert "gemini_image3_pro" == record.package.workflow_model_stack.runway_image_model_id
    assert "GPT 5.5" == record.package.workflow_model_stack.llm_text_generation
    assert "floating city" in record.package.video_prompt.lower()
    assert "floating city" in record.package.av_director_packet.audience_signal.lower()
    assert "audio" in record.package.video_prompt.lower()
    assert saved_path.exists()


def test_redirects_risky_comment():
    comment_input = CommentInput(selected_comment="Make the AI destroy a real city with storms")

    record = create_episode_record(comment_input)

    assert record.guardrail.status == "approved_with_redirect"
    assert "fictional" in record.guardrail.safe_interpretation.lower()
