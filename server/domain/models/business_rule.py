from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class RuleType(str, Enum):
    condition = "condition"
    calculation = "calculation"
    validation = "validation"


@dataclass
class SourceLocation:
    file_path: str
    start_line: int | None = None
    end_line: int | None = None


@dataclass
class BusinessRule:
    id: UUID
    job_id: UUID
    source_file_id: UUID | None
    rule_type: RuleType
    description: str
    source_location: SourceLocation | None
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.description or not self.description.strip():
            raise ValueError("description must not be empty or whitespace only")
