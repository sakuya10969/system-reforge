from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class ProjectCreateRequest(BaseModel):
    name: str
    description: str | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("name must not be empty or whitespace only")
        if len(v) > 255:
            raise ValueError("name must not exceed 255 characters")
        return v


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    s3_prefix: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginationResponse(BaseModel):
    total: int
    page: int
    per_page: int


class ProjectListResponse(BaseModel):
    data: list[ProjectResponse]
    pagination: PaginationResponse
