from abc import ABC, abstractmethod
from uuid import UUID

from server.domain.models.dependency_edge import DependencyEdge


class DependencyEdgeRepository(ABC):
    @abstractmethod
    async def find_by_job(self, job_id: UUID) -> list[DependencyEdge]: ...

    @abstractmethod
    async def create_many(self, edges: list[DependencyEdge]) -> list[DependencyEdge]: ...
