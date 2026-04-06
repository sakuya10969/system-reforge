from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class SourceFile:
    id: UUID
    project_id: UUID
    file_path: str
    language: str | None
    s3_key: str
    created_at: datetime
