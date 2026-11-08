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


def test_pipeline_cross_platform_dry_run():
    release = ReleaseInfo(
        repository="test-repo",
        tag_name="v1.0.0",
        name="Test 1.0.0",
        body="- feat(engine): New cross platform pipeline",
    )

    pipeline = ContentOpsPipeline()
    result = pipeline.run_cross_platform(
        release=release,
        organization_id="org_123",
        linkedin_channel_id="li_123",
        instagram_channel_id="ig_123",
        dry_run=True,
    )

    assert result.success is True
    assert result.status == "cross_platform_dispatched"
    assert len(result.channels) == 2
    assert "li_123" in result.channels
    assert "ig_123" in result.channels
