from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class RequirementStatus(str, Enum):
    draft = "draft"
    reviewed = "reviewed"
    approved = "approved"


class RequirementPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


@dataclass
class Requirement:
    id: UUID
    job_id: UUID
    title: str
    description: str
    category: str | None
    priority: RequirementPriority
    status: RequirementStatus
    source_rules: list[str]
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("title must not be empty or whitespace only")
        if not self.description or not self.description.strip():
            raise ValueError("description must not be empty or whitespace only")
        if not isinstance(self.status, RequirementStatus):
            raise ValueError(f"Invalid status: {self.status}")
        if not isinstance(self.priority, RequirementPriority):
            raise ValueError(f"Invalid priority: {self.priority}")
