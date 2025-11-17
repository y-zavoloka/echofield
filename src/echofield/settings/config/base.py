from __future__ import annotations

from typing import Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Typed application settings configuration.

    Settings are read from environment variables or .env file with defaults and validation.
    All settings can be overridden via environment variables using the same names.

    Example:
        # In .env file:
        DEBUG=true
        SECRET_KEY=your-secret-key-here
        DATABASE_URL=postgresql://user:pass@localhost/db

        # In code:
        settings = AppSettings()
        print(settings.DEBUG)  # True
    """

    # Pydantic Settings: reads .env file from repository root (adjust path as needed)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Core Application Settings ---
    DEBUG: bool = False
    """Enable debug mode. Should be False in production."""

    SECRET_KEY: SecretStr = SecretStr("changeme")
    """Django secret key for cryptographic signing. Must be set in production."""

    # Raw comma-separated values; Django settings module will split to lists.
    ALLOWED_HOSTS: Optional[str] = Field(default=None)
    """Comma-separated list of allowed hostnames (e.g. "example.com,.example.com")."""

    CSRF_TRUSTED_ORIGINS: Optional[str] = Field(default=None)
    """Comma-separated list of trusted origins (e.g. "https://a.com,https://b.com")."""

    LANGUAGE_CODE: str = "en-us"
    """Default language code for the application."""

    TIME_ZONE: str = "Europe/Kyiv"
    """Default timezone for the application."""

    USE_I18N: bool = True
    """Enable Django's internationalization system."""

    USE_TZ: bool = True
    """Enable timezone-aware datetimes."""

    # --- SSL / Security Settings ---
    USE_SSL: bool = False
    """Enable SSL/HTTPS security settings. Set to True in production with HTTPS."""

    # --- Sentry / Error monitoring ---
    SENTRY_DSN: Optional[str] = None
    """Sentry DSN URL; if unset, Sentry is disabled."""

    SENTRY_ENVIRONMENT: str = "local"
    """Sentry environment name (e.g. 'local', 'staging', 'production')."""

    SENTRY_TRACES_SAMPLE_RATE: float = 0.0
    """Sample rate for performance tracing (0–1)."""

    SENTRY_PROFILES_SAMPLE_RATE: float = 0.0
    """Sample rate for profiling (0–1)."""

    # --- Database Configuration ---
    DATABASE_URL: Optional[str] = None
    """Complete database URL (e.g., postgresql://user:pass@host:port/dbname).
    If provided, takes precedence over individual DB_* settings."""

    DB_NAME: Optional[str] = None
    """Database name."""

    DB_USER: Optional[str] = None
    """Database username."""

    DB_PASSWORD: Optional[str] = None
    """Database password."""

    DB_HOST: str = "db"
    """Database host. Defaults to 'db' for Docker environments."""

    DB_PORT: int = 5432
    """Database port. Defaults to 5432 for PostgreSQL."""

    # --- Static/Media Storage (Cloudflare R2 or local) ---
    USE_R2_STATIC: bool = False
    """Enable Cloudflare R2 for static file storage. If False, uses local storage."""

    R2_CUSTOM_DOMAIN: Optional[str] = None
    """Custom domain for R2 bucket (e.g., 'static.example.com')."""

    R2_BUCKET: Optional[str] = None
    """R2 bucket name for static files."""

    R2_ENDPOINT: Optional[str] = None
    """R2 endpoint URL (e.g., 'https://account-id.r2.cloudflarestorage.com')."""

    R2_ACCESS_KEY_ID: Optional[str] = None
    """R2 access key ID for authentication."""

    R2_SECRET_ACCESS_KEY: Optional[str] = None
    """R2 secret access key for authentication."""
