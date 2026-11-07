"""Tests for Buffer CLI runner and GraphQL client."""

from buffer_content_ops.buffer.cli_runner import BufferCliRunner
from buffer_content_ops.buffer.graphql_client import BufferGraphQLClient
from buffer_content_ops.models import BufferMutationPayload


def test_cli_runner_dry_run():
    runner = BufferCliRunner()
    payload = BufferMutationPayload(
        channel_id="test_channel",
        text="Hello LinkedIn!",
        dry_run=True,
    )
    result = runner.create_post(payload)
    assert result["dryRun"] is True
    # Should safely succeed or return dry-run output
    assert "exitCode" in result


def test_graphql_client_mock():
    client = BufferGraphQLClient(api_key=None)
    account = client.get_account()
    assert account["mock"] is True
    assert "organizations" in account["account"]

    channels = client.list_channels()
    assert len(channels) == 1
    assert channels[0].service == "linkedin"
