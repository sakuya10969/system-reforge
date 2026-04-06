from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Project:
    id: UUID
    name: str
    description: str | None
    s3_prefix: str
    created_at: datetime
    updated_at: datetime
