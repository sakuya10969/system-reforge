from abc import ABC, abstractmethod
from uuid import UUID

from server.domain.models.project import Project


class ProjectRepository(ABC):
    @abstractmethod
    async def create(self, project: Project) -> Project: ...

    @abstractmethod
    async def find_by_id(self, project_id: UUID) -> Project | None: ...

    @abstractmethod
    async def find_all(self, page: int, per_page: int) -> tuple[list[Project], int]: ...

    @abstractmethod
    async def delete(self, project_id: UUID) -> bool: ...
