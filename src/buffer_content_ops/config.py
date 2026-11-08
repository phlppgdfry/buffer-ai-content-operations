"""Configuration management using environment variables and Buffer CLI settings."""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for Buffer Content Operations."""

    buffer_api_key: str | None = None
    buffer_organization_id: str | None = None
    buffer_linkedin_channel_id: str | None = None
    buffer_instagram_channel_id: str | None = None
    buffer_post_mode: str = "draft"  # draft | addToQueue | customScheduled
    github_token: str | None = None

    # CLI path resolution
    buffer_cli_path: str = "buffer"
    gh_cli_path: str = "gh"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> Settings:
    """Retrieve settings instance with fallback to Buffer CLI environment."""
    settings = Settings()
    if not settings.buffer_api_key:
        # Check standard BUFFER_API_KEY environment variable
        settings.buffer_api_key = os.environ.get("BUFFER_API_KEY")
    return settings
