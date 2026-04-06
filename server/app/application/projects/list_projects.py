from app.domain.models.project import Project
from app.domain.repositories.project_repository import ProjectRepository


class ListProjectsUseCase:
    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    async def execute(self, page: int = 1, per_page: int = 20) -> tuple[list[Project], int]:
        return await self._repository.find_all(page=page, per_page=per_page)
