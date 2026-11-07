"""Tests for multi-agent synthesis and quality gate."""

from buffer_content_ops.agents.business_story import BusinessStoryAgent
from buffer_content_ops.agents.quality_gate import QualityGateAgent
from buffer_content_ops.agents.tech_extractor import TechExtractorAgent
from buffer_content_ops.models import ReleaseInfo


def test_agent_synthesis_flow():
    release = ReleaseInfo(
        repository="phlppgdfry/agentic-workflow-platform",
        tag_name="v2.0.0",
        name="Version 2.0.0",
        body=(
            "- feat(core): Asynchronous event broker with Python and FastAPI\n"
            "- perf(cache): 50% decrease in response latency\n"
            "- fix(auth): Resolved token expiry edge case\n"
        ),
    )

    tech_agent = TechExtractorAgent()
    insights = tech_agent.analyze(release)
    assert len(insights.features) > 0
    assert "Python" in insights.stack

    story_agent = BusinessStoryAgent()
    narrative = story_agent.compose("agentic-workflow-platform", insights)
    assert "#BufferAPI" in narrative.hashtags
    assert "The Challenge" in narrative.to_formatted_post()

    quality_agent = QualityGateAgent()
    review = quality_agent.evaluate(narrative)
    assert review.passed is True
    assert review.score >= 80
    assert review.char_count < 3000
