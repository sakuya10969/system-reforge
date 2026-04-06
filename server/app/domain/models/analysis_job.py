from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID

from app.domain.exceptions import InvalidStatusTransitionError


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"


VALID_TRANSITIONS: dict[JobStatus, set[JobStatus]] = {
    JobStatus.pending: {JobStatus.running},
    JobStatus.running: {JobStatus.completed, JobStatus.failed},
    JobStatus.completed: set(),
    JobStatus.failed: set(),
}


@dataclass
class AnalysisJob:
    id: UUID
    project_id: UUID
    status: JobStatus
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None

    def transition_to(self, new_status: JobStatus, **kwargs) -> None:
        if new_status not in VALID_TRANSITIONS[self.status]:
            raise InvalidStatusTransitionError(
                f"Cannot transition from {self.status} to {new_status}"
            )
        self.status = new_status
        if new_status == JobStatus.running:
            self.started_at = kwargs.get("started_at")
        elif new_status == JobStatus.completed:
            self.completed_at = kwargs.get("completed_at")
        elif new_status == JobStatus.failed:
            self.error_message = kwargs.get("error_message")
            self.completed_at = kwargs.get("completed_at")
