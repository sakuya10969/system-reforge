from uuid import UUID

from app.domain.exceptions import ProjectNotFoundError
from app.domain.repositories.project_repository import ProjectRepository


class DeleteProjectUseCase:
    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    async def execute(self, project_id: UUID) -> None:
        deleted = await self._repository.delete(project_id)
        if not deleted:
            raise ProjectNotFoundError(f"Project {project_id} not found")
