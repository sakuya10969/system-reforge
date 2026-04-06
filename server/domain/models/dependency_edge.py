from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID


class DependencyType(str, Enum):
    CALL = "CALL"
    COPY = "COPY"
    INCLUDE = "INCLUDE"


@dataclass
class DependencyEdge:
    id: UUID
    job_id: UUID
    source_file_id: UUID
    target_file_id: UUID
    dependency_type: DependencyType
    metadata: dict = field(default_factory=dict)
