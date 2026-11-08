"""Core data contracts and schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ReleaseInfo(BaseModel):
    """Normalized release or changelog payload."""

    repository: str
    tag_name: str
    name: str
    body: str
    html_url: str | None = None
    published_at: datetime | None = None
    commits: list[str] = Field(default_factory=list)
    pr_numbers: list[int] = Field(default_factory=list)


class TechnicalInsights(BaseModel):
    """Output of Technical Extraction Agent."""

    primary_theme: str
    features: list[str] = Field(default_factory=list)
    optimizations: list[str] = Field(default_factory=list)
    fixes: list[str] = Field(default_factory=list)
    breaking_changes: list[str] = Field(default_factory=list)
    architecture_notes: str | None = None
    stack: list[str] = Field(default_factory=list)


class BusinessNarrative(BaseModel):
    """Output of Business Storytelling Agent."""

    hook: str
    problem_statement: str
    solution_summary: str
    measurable_impact: str
    call_to_action: str
    hashtags: list[str] = Field(default_factory=list)

    def to_formatted_post(self) -> str:
        """Compose into high-impact LinkedIn post format (under 3000 chars)."""
        tags_str = " ".join(self.hashtags)
        return (
            f"{self.hook}\n\n"
            f"🎯 The Challenge:\n{self.problem_statement}\n\n"
            f"💡 What We Built:\n{self.solution_summary}\n\n"
            f"📈 Business & Engineering Impact:\n{self.measurable_impact}\n\n"
            f"{self.call_to_action}\n\n"
            f"{tags_str}"
        ).strip()


class QualityGateReview(BaseModel):
    """Output of Content Quality & Compliance Gate."""

    score: int = Field(ge=0, le=100)
    passed: bool
    char_count: int
    readability: str
    checks: dict[str, bool] = Field(default_factory=dict)
    feedback: list[str] = Field(default_factory=list)


class BufferChannel(BaseModel):
    """Metadata for a connected social channel in Buffer."""

    id: str
    service: str  # linkedin, instagram, twitter, etc.
    name: str
    formatted_service: str | None = None
    organization_id: str | None = None
    is_disconnected: bool = False


class BufferMutationPayload(BaseModel):
    """Payload sent to Buffer posts.create mutation."""

    channel_id: str
    text: str
    save_to_draft: bool = True
    ai_assisted: bool = True
    mode: str = "addToQueue"  # addToQueue, customScheduled, shareNow
    scheduling_type: str = "automatic"
    dry_run: bool = False


class PipelineResult(BaseModel):
    """Final result of end-to-end execution."""

    success: bool
    channel: str
    post_id: str | None = None
    status: str
    narrative: BusinessNarrative
    quality_review: QualityGateReview
    raw_buffer_response: dict[str, Any] | None = None
    error_message: str | None = None


class PostVariant(BaseModel):
    """Channel-specific variant within a multi-channel content item."""

    channel_id: str
    text: str
    mode: str = "addToQueue"
    scheduling_type: str = "automatic"
    save_to_draft: bool = True
    ai_assisted: bool = True
    image_url: str | None = None


class BufferContentItemPayload(BaseModel):
    """Payload sent to Buffer contentItems.create mutation for cross-posting."""

    organization_id: str
    title: str | None = None
    posts: list[PostVariant] = Field(default_factory=list)
    dry_run: bool = False


class MultiChannelPipelineResult(BaseModel):
    """Result of cross-platform (Instagram & LinkedIn) dispatch."""

    success: bool
    content_item_id: str | None = None
    channels: list[str] = Field(default_factory=list)
    status: str
    narrative: BusinessNarrative
    quality_review: QualityGateReview
    raw_buffer_response: dict[str, Any] | None = None
    error_message: str | None = None
