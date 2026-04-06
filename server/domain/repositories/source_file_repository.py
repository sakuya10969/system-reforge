from abc import ABC, abstractmethod
from uuid import UUID

from server.domain.models.source_file import SourceFile


class SourceFileRepository(ABC):
    @abstractmethod
    async def create_many(self, files: list[SourceFile]) -> list[SourceFile]: ...

    @abstractmethod
    async def find_by_project(self, project_id: UUID) -> list[SourceFile]: ...

    @abstractmethod
    async def find_by_id(self, file_id: UUID) -> SourceFile | None: ...
