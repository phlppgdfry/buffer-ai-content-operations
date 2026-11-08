"""End-to-End Content Operations Orchestration Pipeline."""

from collections.abc import Callable

from .agents.business_story import BusinessStoryAgent
from .agents.quality_gate import QualityGateAgent
from .agents.tech_extractor import TechExtractorAgent
from .buffer.cli_runner import BufferCliRunner
from .buffer.graphql_client import BufferGraphQLClient
from .models import (
    BufferContentItemPayload,
    BufferMutationPayload,
    BusinessNarrative,
    MultiChannelPipelineResult,
    PipelineResult,
    PostVariant,
    QualityGateReview,
    ReleaseInfo,
)


class ContentOpsPipeline:
    """Orchestrates multi-agent technical transformation to Buffer draft."""

    def __init__(
        self,
        tech_agent: TechExtractorAgent | None = None,
        story_agent: BusinessStoryAgent | None = None,
        quality_agent: QualityGateAgent | None = None,
        cli_runner: BufferCliRunner | None = None,
        api_client: BufferGraphQLClient | None = None,
    ):
        self.tech_agent = tech_agent or TechExtractorAgent()
        self.story_agent = story_agent or BusinessStoryAgent()
        self.quality_agent = quality_agent or QualityGateAgent()
        self.cli_runner = cli_runner or BufferCliRunner()
        self.api_client = api_client or BufferGraphQLClient()

    def run(
        self,
        release: ReleaseInfo,
        channel_id: str | None = None,
        dry_run: bool = True,
        approval_callback: Callable[[BusinessNarrative, QualityGateReview], bool] | None = None,
        use_graphql_direct: bool = False,
    ) -> PipelineResult:
        """Execute full content operations pipeline."""
        # Step 1: Technical Extraction
        insights = self.tech_agent.analyze(release)

        # Step 2: Business Storytelling Narrative
        narrative = self.story_agent.compose(repo_name=release.repository, insights=insights)

        # Step 3: Quality Gate Evaluation
        quality_review = self.quality_agent.evaluate(narrative)
        if not quality_review.passed:
            return PipelineResult(
                success=False,
                channel=channel_id or "unassigned",
                status="rejected_by_quality_gate",
                narrative=narrative,
                quality_review=quality_review,
                error_message="; ".join(quality_review.feedback),
            )

        # Step 4: Human-in-the-loop Governance Gate
        if approval_callback:
            approved = approval_callback(narrative, quality_review)
            if not approved:
                return PipelineResult(
                    success=False,
                    channel=channel_id or "unassigned",
                    status="rejected_by_human_reviewer",
                    narrative=narrative,
                    quality_review=quality_review,
                    error_message="Post draft was rejected during human review.",
                )

        # Step 5: Buffer Social Dispatch (Always default to draft for maximum safety)
        target_channel = channel_id or "mock_linkedin_channel_01"
        payload = BufferMutationPayload(
            channel_id=target_channel,
            text=narrative.to_formatted_post(),
            save_to_draft=True,
            ai_assisted=True,
            mode="addToQueue",
            dry_run=dry_run,
        )

        if use_graphql_direct:
            raw_response = self.api_client.create_draft_mutation(payload)
            post_id = (
                raw_response.get("data", {})
                .get("createPost", {})
                .get("post", {})
                .get("id", "api_draft_registered")
            )
        else:
            raw_response = self.cli_runner.create_post(payload)
            post_id = (
                raw_response.get("data", {})
                .get("post", {})
                .get("id", "cli_draft_created" if not dry_run else "dry_run_validated")
            )

        is_success = raw_response.get("success", True) or dry_run

        return PipelineResult(
            success=is_success,
            channel=target_channel,
            post_id=post_id,
            status="draft_created" if not dry_run else "dry_run_success",
            narrative=narrative,
            quality_review=quality_review,
            raw_buffer_response=raw_response,
        )

    def run_cross_platform(
        self,
        release: ReleaseInfo,
        organization_id: str,
        linkedin_channel_id: str,
        instagram_channel_id: str,
        instagram_image_url: str = "https://www.reviewell.com/reviewell-icon.png",
        dry_run: bool = True,
        save_to_draft: bool = True,
        approval_callback: Callable[[BusinessNarrative, QualityGateReview], bool] | None = None,
    ) -> MultiChannelPipelineResult:
        """Execute multi-channel cross-dispatch targeting both Instagram and LinkedIn.

        Qualifies for the official 'Instagram & LinkedIn Publisher' capability.
        """
        # Step 1: Technical Extraction
        insights = self.tech_agent.analyze(release)

        # Step 2: Narrative Generation
        narrative = self.story_agent.compose(repo_name=release.repository, insights=insights)

        # Step 3: Quality Gate
        quality_review = self.quality_agent.evaluate(narrative)
        if not quality_review.passed:
            return MultiChannelPipelineResult(
                success=False,
                channels=[linkedin_channel_id, instagram_channel_id],
                status="rejected_by_quality_gate",
                narrative=narrative,
                quality_review=quality_review,
                error_message="; ".join(quality_review.feedback),
            )

        # Step 4: Governance Gate
        if approval_callback:
            approved = approval_callback(narrative, quality_review)
            if not approved:
                return MultiChannelPipelineResult(
                    success=False,
                    channels=[linkedin_channel_id, instagram_channel_id],
                    status="rejected_by_human_reviewer",
                    narrative=narrative,
                    quality_review=quality_review,
                    error_message="Multi-channel dispatch rejected by human reviewer.",
                )

        # Step 5: Multi-Channel Content Item Dispatch
        content_payload = BufferContentItemPayload(
            organization_id=organization_id,
            title=f"Cross-Platform Release: {release.name}",
            dry_run=dry_run,
            posts=[
                PostVariant(
                    channel_id=linkedin_channel_id,
                    text=narrative.to_formatted_post(),
                    mode="addToQueue",
                    scheduling_type="automatic",
                    save_to_draft=save_to_draft,
                    ai_assisted=True,
                ),
                PostVariant(
                    channel_id=instagram_channel_id,
                    text=narrative.to_formatted_post(),
                    mode="addToQueue",
                    scheduling_type="automatic",
                    save_to_draft=save_to_draft,
                    ai_assisted=True,
                    image_url=instagram_image_url,
                ),
            ],
        )

        raw_response = self.cli_runner.create_content_item(content_payload)
        is_success = raw_response.get("success", False) or dry_run

        content_item_id = None
        if not dry_run and is_success:
            data = raw_response.get("data", {})
            content_obj = data.get("content") or data.get("createContentItem", {}).get("content", {})
            content_item_id = content_obj.get("id") if isinstance(content_obj, dict) else None

        return MultiChannelPipelineResult(
            success=is_success,
            content_item_id=content_item_id or ("dry_run_item_id" if dry_run else None),
            channels=[linkedin_channel_id, instagram_channel_id],
            status="cross_platform_dispatched" if is_success else "failed",
            narrative=narrative,
            quality_review=quality_review,
            raw_buffer_response=raw_response,
            error_message=raw_response.get("error"),
        )
