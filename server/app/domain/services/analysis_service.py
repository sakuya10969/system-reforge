from abc import ABC, abstractmethod
from uuid import UUID


class AnalysisService(ABC):
    @abstractmethod
    async def analyze(self, job_id: UUID, project_id: UUID) -> None: ...
