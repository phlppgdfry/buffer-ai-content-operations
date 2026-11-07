"""Tests for end-to-end pipeline."""

from buffer_content_ops.models import ReleaseInfo
from buffer_content_ops.pipeline import ContentOpsPipeline


def test_pipeline_dry_run_with_approval():
    release = ReleaseInfo(
        repository="test-repo",
        tag_name="v1.0.0",
        name="Test 1.0.0",
        body="- feat(engine): New agent pipeline",
    )

    approval_called = False

    def on_review(narrative, review):
        nonlocal approval_called
        approval_called = True
        return True

    pipeline = ContentOpsPipeline()
    result = pipeline.run(
        release,
        channel_id="ch_123",
        dry_run=True,
        approval_callback=on_review,
    )

    assert approval_called is True
    assert result.success is True
    assert result.status == "dry_run_success"
    assert result.channel == "ch_123"
