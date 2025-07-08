"""Configuration settings for KHTRM System backend."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application settings
    app_name: str = Field(default="KHTRM System", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")

    # Server settings
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port")
    reload: bool = Field(default=False, description="Auto-reload on changes")

    # Security settings
    secret_key: str = Field(
        default="your-secret-key-change-this-in-production",
        description="Secret key for JWT token generation",
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30, description="Access token expiration time in minutes"
    )

    # Database settings
    database_url: str = Field(
        default="sqlite:///./khtrm_system.db",
        description="Database connection URL",
    )
    database_echo: bool = Field(default=False, description="Echo SQL queries")

    # MySQL specific settings (when using MySQL)
    mysql_host: str | None = Field(default=None, description="MySQL host")
    mysql_port: int | None = Field(default=3306, description="MySQL port")
    mysql_user: str | None = Field(default=None, description="MySQL username")
    mysql_password: str | None = Field(default=None, description="MySQL password")
    mysql_database: str | None = Field(default=None, description="MySQL database name")

    # CORS settings
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )
    cors_credentials: bool = Field(default=True, description="Allow credentials")
    cors_methods: list[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Allowed HTTP methods",
    )
    cors_headers: list[str] = Field(default=["*"], description="Allowed headers")

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str | None = Field(default=None, description="Log file path")

    # Pagination settings
    default_page_size: int = Field(default=20, description="Default page size")
    max_page_size: int = Field(default=100, description="Maximum page size")

    # File upload settings
    upload_dir: str = Field(default="uploads", description="Upload directory")
    max_file_size: int = Field(
        default=10 * 1024 * 1024, description="Max file size (10MB)"
    )

    # Email settings (for future use)
    smtp_server: str | None = Field(default=None, description="SMTP server")
    smtp_port: int | None = Field(default=587, description="SMTP port")
    smtp_username: str | None = Field(default=None, description="SMTP username")
    smtp_password: str | None = Field(default=None, description="SMTP password")
    smtp_tls: bool = Field(default=True, description="Use TLS")

    @property
    def mysql_url(self) -> str:
        """Generate MySQL connection URL."""
        if all(
            [self.mysql_host, self.mysql_user, self.mysql_password, self.mysql_database]
        ):
            return (
                f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
                f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
                f"?charset=utf8mb4"
            )
        return self.database_url

    @property
    def effective_database_url(self) -> str:
        """Get effective database URL (MySQL if configured, otherwise SQLite)."""
        return self.mysql_url if self.mysql_host else self.database_url


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
