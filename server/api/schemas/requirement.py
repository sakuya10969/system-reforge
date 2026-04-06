from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class RequirementResponse(BaseModel):
    id: UUID
    job_id: UUID
    title: str
    description: str
    category: str | None
    priority: str
    status: str
    source_rules: list[str]
    created_at: datetime
    updated_at: datetime


class RequirementListResponse(BaseModel):
    data: list[RequirementResponse]


class RequirementUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    priority: str | None = None
    status: str | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("title must not be empty")
        return v

    @field_validator("description")
    @classmethod
    def description_must_not_be_blank(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("description must not be empty")
        return v


class ExportData(BaseModel):
    markdown: str


class ExportResponse(BaseModel):
    data: ExportData
