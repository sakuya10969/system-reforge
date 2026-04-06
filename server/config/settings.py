from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    aws_access_key_id: str | None = Field(default=None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str | None = Field(default=None, alias="AWS_SECRET_ACCESS_KEY")
    aws_default_region: str | None = Field(default=None, alias="AWS_DEFAULT_REGION")
    aws_bedrock_region: str | None = Field(default=None, alias="AWS_BEDROCK_REGION")
    aws_bedrock_model_id: str | None = Field(default=None, alias="AWS_BEDROCK_MODEL_ID")
    s3_bucket_name: str = Field(default="system-reforge", alias="S3_BUCKET_NAME")

    @property
    def s3_region(self) -> str | None:
        return self.aws_default_region or self.aws_bedrock_region

    @property
    def bedrock_region(self) -> str | None:
        return self.aws_bedrock_region or self.aws_default_region

    @property
    def use_bedrock(self) -> bool:
        return bool(self.aws_bedrock_model_id)


@lru_cache
def get_settings() -> Settings:
    return Settings()
