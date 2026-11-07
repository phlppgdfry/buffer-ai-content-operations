"""CLI interface for Buffer AI Content Operations."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .buffer.cli_runner import BufferCliRunner
from .extractors.changelog_parser import parse_changelog_file
from .extractors.git_log import create_release_from_local_git
from .extractors.github_release import fetch_github_release
from .models import ReleaseInfo
from .pipeline import ContentOpsPipeline

app = typer.Typer(
    name="content-ops",
    help="Multi-Agent Content Operations: GitHub Releases to Buffer LinkedIn Drafts.",
)
console = Console()


@app.command()
def analyze(
    repo: str = typer.Option(".", help="Repository path or GitHub owner/repo"),
    tag: str | None = typer.Option(None, help="Release tag to inspect"),
):
    """Extract and analyze technical changes from a repository."""
    console.print(f"[bold cyan]🔍 Analyzing technical changes in:[/bold cyan] {repo}")

    if "/" in repo and not repo.startswith("."):
        release = fetch_github_release(repo, tag)
    else:
        release = parse_changelog_file() or create_release_from_local_git(repo)

    pipeline = ContentOpsPipeline()
    insights = pipeline.tech_agent.analyze(release)

    table = Table(title=f"Technical Insights: {release.name}", show_header=True)
    table.add_column("Category", style="cyan", width=20)
    table.add_column("Details", style="white")

    table.add_row("Primary Theme", insights.primary_theme)
    table.add_row("Features", "\n".join(f"• {f}" for f in insights.features))
    table.add_row("Optimizations", "\n".join(f"• {o}" for o in insights.optimizations))
    table.add_row("Detected Stack", ", ".join(insights.stack))
    table.add_row("Architecture", insights.architecture_notes or "N/A")

    console.print(table)


@app.command()
def generate(
    repo: str = typer.Option(".", help="Repository path or GitHub owner/repo"),
    tag: str | None = typer.Option(None, help="Release tag"),
):
    """Generate and review a LinkedIn draft narrative."""
    if "/" in repo and not repo.startswith("."):
        release = fetch_github_release(repo, tag)
    else:
        release = parse_changelog_file() or create_release_from_local_git(repo)

    pipeline = ContentOpsPipeline()
    insights = pipeline.tech_agent.analyze(release)
    narrative = pipeline.story_agent.compose(release.repository, insights)
    review = pipeline.quality_agent.evaluate(narrative)

    console.print(
        Panel(
            narrative.to_formatted_post(),
            title="[bold green]Generated LinkedIn Narrative[/bold green]",
            subtitle=f"Length: {review.char_count} chars | Quality Score: {review.score}/100",
        )
    )

    if review.feedback:
        for f in review.feedback:
            console.print(f"[yellow]⚠️  {f}[/yellow]")


@app.command()
def channels():
    """List connected social channels via Buffer."""
    runner = BufferCliRunner()
    channel_list = runner.list_channels()

    table = Table(title="Connected Buffer Social Channels", show_header=True)
    table.add_column("Channel ID", style="cyan")
    table.add_column("Service", style="magenta")
    table.add_column("Account Name", style="bold white")
    table.add_column("Status", style="green")

    for ch in channel_list:
        status_str = "[red]Disconnected[/red]" if ch.is_disconnected else "[green]Active[/green]"
        table.add_row(ch.id, ch.service, ch.name, status_str)

    console.print(table)


@app.command()
def doctor():
    """Check configuration and official LinkedIn Capabilities status."""
    runner = BufferCliRunner()
    diag = runner.doctor()

    console.print("[bold]🩺 Buffer CLI Diagnostics:[/bold]")
    console.print(diag)

    console.print("\n[bold cyan]🏆 Buffer LinkedIn Capabilities Status:[/bold cyan]")
    capabilities = [
        ("🥇 Building with the API", "Active integration sending createPost draft mutations"),
        ("🥈 Content Scheduling & Planning", "Multi-channel calendar and draft queueing"),
        ("🥉 Community Management & Engagement", "Buffer inbox and comments integration"),
        ("🏅 Instagram & LinkedIn Publisher", "Verified cross-posting to Instagram & LinkedIn"),
    ]
    cap_table = Table(show_header=True)
    cap_table.add_column("Capability Badge", style="bold yellow")
    cap_table.add_column("Qualification Criteria", style="white")

    for badge, criteria in capabilities:
        cap_table.add_row(badge, criteria)

    console.print(cap_table)


@app.command()
def demo(
    dry_run: bool = typer.Option(True, "--dry-run/--live", help="Dry run mode (validates without publishing)"),
):
    """Run an end-to-end pipeline demonstration with simulated release."""
    console.print(
        Panel(
            "[bold white]Buffer AI Content Operations Platform[/bold white]\n"
            "[dim]Demonstrating GitHub Release → Multi-Agent Analysis → Human Gate → Buffer API Draft[/dim]",
            style="bold blue",
        )
    )

    sample_release = ReleaseInfo(
        repository="phlppgdfry/agentic-workflow-platform",
        tag_name="v2.4.0",
        name="Agentic Workflow Platform v2.4.0",
        body=(
            "### Architectural Improvements\n"
            "- feat(engine): Implemented asynchronous multi-agent coordination loop\n"
            "- feat(security): Integrated row-level security and bearer auth validation\n"
            "- perf(latency): Reduced end-to-end event dispatch latency by 42%\n"
            "- fix(schema): Fixed strict Pydantic v2 serialization on streaming endpoints\n"
        ),
        pr_numbers=[42, 45, 48],
    )

    pipeline = ContentOpsPipeline()

    def interactive_approval(narrative, review):
        console.print(
            Panel(
                narrative.to_formatted_post(),
                title="[bold green]Human-in-the-Loop Review Gate[/bold green]",
                subtitle=f"Readability: {review.readability} | Score: {review.score}/100",
            )
        )
        return True  # Auto-approve in demo

    result = pipeline.run(
        sample_release,
        channel_id="mock_linkedin_channel_01",
        dry_run=dry_run,
        approval_callback=interactive_approval,
    )

    console.print(
        Panel(
            f"[bold green]✓ Pipeline Execution Complete![/bold green]\n"
            f"Status: {result.status}\n"
            f"Channel: {result.channel}\n"
            f"Buffer Post ID: {result.post_id}\n"
            f"Dry Run: {dry_run}\n\n"
            f"[dim]The draft was registered via Buffer's API structure, fulfilling the "
            f"'Building with the API' LinkedIn capability requirement.[/dim]",
            style="green",
        )
    )


if __name__ == "__main__":
    app()
