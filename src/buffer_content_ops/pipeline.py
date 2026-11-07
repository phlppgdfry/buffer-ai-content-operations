"""End-to-End Content Operations Orchestration Pipeline."""

from collections.abc import Callable

from .agents.business_story import BusinessStoryAgent
from .agents.quality_gate import QualityGateAgent
from .agents.tech_extractor import TechExtractorAgent
from .buffer.cli_runner import BufferCliRunner
from .buffer.graphql_client import BufferGraphQLClient
from .models import (
    BufferMutationPayload,
    BusinessNarrative,
    PipelineResult,
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
