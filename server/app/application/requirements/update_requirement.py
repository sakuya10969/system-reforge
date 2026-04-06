from datetime import datetime, timezone
from uuid import UUID

from app.domain.exceptions import RequirementNotFoundError
from app.domain.models.requirement import Requirement, RequirementPriority, RequirementStatus
from app.domain.repositories.requirement_repository import RequirementRepository


class UpdateRequirementUseCase:
    def __init__(self, repository: RequirementRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        requirement_id: UUID,
        title: str | None = None,
        description: str | None = None,
        category: str | None = None,
        priority: str | None = None,
        status: str | None = None,
    ) -> Requirement:
        requirement = await self._repository.find_by_id(requirement_id)
        if requirement is None:
            raise RequirementNotFoundError(f"Requirement {requirement_id} not found")

        if title is not None:
            if not title.strip():
                raise ValueError("title must not be empty")
            requirement.title = title.strip()
        if description is not None:
            if not description.strip():
                raise ValueError("description must not be empty")
            requirement.description = description.strip()
        if category is not None:
            requirement.category = category
        if priority is not None:
            requirement.priority = RequirementPriority(priority)
        if status is not None:
            requirement.status = RequirementStatus(status)
        requirement.updated_at = datetime.now(timezone.utc)

        return await self._repository.update(requirement)
