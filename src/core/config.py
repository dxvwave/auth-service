from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # Database
    database_url: str = Field(
        ...,
        description="Database connection URL",
    )

    # JWT Configuration
    jwt_secret_key: str = Field(
        ...,
        description="Secret key for JWT token generation",
        min_length=32,
    )
    jwt_algorithm: str = Field(
        default="HS256",
        description="Algorithm for JWT token generation",
    )
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes",
        gt=0,
        le=1440,  # Max 24 hours
    )
    jwt_refresh_token_expire_days: int = Field(
        default=7,
        description="Refresh token expiration time in days",
        gt=0,
        le=30,  # Max 30 days
    )

    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    @field_validator("jwt_algorithm")
    @classmethod
    def validate_algorithm(cls, v: str) -> str:
        """Validate JWT algorithm."""
        allowed = ["HS256", "HS384", "HS512"]
        if v not in allowed:
            raise ValueError(f"Algorithm must be one of {allowed}")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in allowed:
            raise ValueError(f"Log level must be one of {allowed}")
        return v_upper


settings = Settings()
