from uuid import UUID

from app.domain.exceptions import ProjectNotFoundError
from app.domain.models.analysis_job import AnalysisJob
from app.domain.repositories.analysis_job_repository import AnalysisJobRepository
from app.domain.repositories.project_repository import ProjectRepository


class ListJobsUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        job_repository: AnalysisJobRepository,
    ) -> None:
        self._project_repository = project_repository
        self._job_repository = job_repository

    async def execute(self, project_id: UUID) -> list[AnalysisJob]:
        project = await self._project_repository.find_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")
        return await self._job_repository.find_by_project(project_id)
