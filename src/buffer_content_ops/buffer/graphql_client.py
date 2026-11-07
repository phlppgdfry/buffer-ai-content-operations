"""Direct Buffer GraphQL API Client.

Provides direct GraphQL integration with the Buffer API to register programmatic
API usage and qualify for the official 'Building with the API' capability.
"""

import os
from typing import Any

import httpx

from ..models import BufferChannel, BufferMutationPayload


class BufferGraphQLClient:
    """Direct GraphQL client for Buffer API."""

    GRAPHQL_ENDPOINT = "https://api.buffer.com"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("BUFFER_API_KEY")

    def _headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Buffer-AI-Content-Operations/0.1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def get_account(self) -> dict[str, Any]:
        """Fetch authenticated account and organizations."""
        query = """
        query GetAccount {
            account {
                id
                email
                name
                timezone
                organizations {
                    id
                    name
                }
            }
        }
        """
        if not self.api_key:
            return {
                "mock": True,
                "account": {
                    "id": "mock_acc_01",
                    "name": "Philippe Godfroy",
                    "timezone": "Europe/Amsterdam",
                    "organizations": [{"id": "mock_org_01", "name": "Godfroy Operations"}],
                },
            }

        with httpx.Client(timeout=10.0) as client:
            resp = client.post(self.GRAPHQL_ENDPOINT, headers=self._headers(), json={"query": query})
            resp.raise_for_status()
            return resp.json()

    def list_channels(self) -> list[BufferChannel]:
        """Query channels via GraphQL."""
        query = """
        query ListChannels {
            channels {
                id
                name
                service
                isDisconnected
                organizationId
            }
        }
        """
        if not self.api_key:
            return [
                BufferChannel(
                    id="mock_linkedin_01",
                    service="linkedin",
                    name="Philippe Godfroy (LinkedIn)",
                    organization_id="mock_org_01",
                )
            ]

        with httpx.Client(timeout=10.0) as client:
            resp = client.post(self.GRAPHQL_ENDPOINT, headers=self._headers(), json={"query": query})
            resp.raise_for_status()
            data = resp.json()
            channels = data.get("data", {}).get("channels", [])
            return [
                BufferChannel(
                    id=c["id"],
                    service=c.get("service", "unknown"),
                    name=c.get("name", "Channel"),
                    organization_id=c.get("organizationId"),
                    is_disconnected=c.get("isDisconnected", False),
                )
                for c in channels
            ]

    def create_draft_mutation(self, payload: BufferMutationPayload) -> dict[str, Any]:
        """Execute createPost mutation saving as draft."""
        mutation = """
        mutation CreatePostDraft($input: CreatePostInput!) {
            createPost(input: $input) {
                ... on PostActionSuccess {
                    post {
                        id
                        status
                        dueAt
                        text
                    }
                }
            }
        }
        """
        variables = {
            "input": {
                "channelId": payload.channel_id,
                "text": payload.text,
                "mode": payload.mode,
                "schedulingType": payload.scheduling_type,
                "saveToDraft": payload.save_to_draft,
                "aiAssisted": payload.ai_assisted,
            }
        }

        if not self.api_key or payload.dry_run:
            return {
                "dry_run": True,
                "data": {
                    "createPost": {
                        "post": {
                            "id": "draft_dry_run_999",
                            "status": "draft",
                            "text": payload.text[:50] + "...",
                        }
                    }
                },
            }

        with httpx.Client(timeout=15.0) as client:
            resp = client.post(
                self.GRAPHQL_ENDPOINT,
                headers=self._headers(),
                json={"query": mutation, "variables": variables},
            )
            resp.raise_for_status()
            return resp.json()
