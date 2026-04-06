from abc import ABC, abstractmethod
from uuid import UUID

from server.domain.models.analysis_job import AnalysisJob


class AnalysisJobRepository(ABC):
    @abstractmethod
    async def create(self, job: AnalysisJob) -> AnalysisJob: ...

    @abstractmethod
    async def find_by_id(self, job_id: UUID) -> AnalysisJob | None: ...

    @abstractmethod
    async def find_by_project(self, project_id: UUID) -> list[AnalysisJob]: ...

    @abstractmethod
    async def update(self, job: AnalysisJob) -> AnalysisJob: ...
