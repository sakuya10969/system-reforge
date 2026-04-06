from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SourceLocationSchema(BaseModel):
    file_path: str
    start_line: int | None = None
    end_line: int | None = None


class BusinessRuleResponse(BaseModel):
    id: UUID
    job_id: UUID
    source_file_id: UUID | None
    rule_type: str
    description: str
    source_location: SourceLocationSchema | None = None
    created_at: datetime


class BusinessRuleListResponse(BaseModel):
    data: list[BusinessRuleResponse]
