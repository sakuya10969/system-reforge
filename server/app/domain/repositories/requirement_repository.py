from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.requirement import Requirement


class RequirementRepository(ABC):
    @abstractmethod
    async def find_by_job(self, job_id: UUID) -> list[Requirement]: ...

    @abstractmethod
    async def find_by_id(self, requirement_id: UUID) -> Requirement | None: ...

    @abstractmethod
    async def update(self, requirement: Requirement) -> Requirement: ...

    @abstractmethod
    async def create_many(self, requirements: list[Requirement]) -> list[Requirement]: ...
