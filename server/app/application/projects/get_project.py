from uuid import UUID

from app.domain.exceptions import ProjectNotFoundError
from app.domain.models.project import Project
from app.domain.repositories.project_repository import ProjectRepository


class GetProjectUseCase:
    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    async def execute(self, project_id: UUID) -> Project:
        project = await self._repository.find_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")
        return project
