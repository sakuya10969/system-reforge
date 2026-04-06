from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions import NoSourceFilesError, ProjectNotFoundError
from app.domain.models.analysis_job import AnalysisJob, JobStatus
from app.domain.repositories.analysis_job_repository import AnalysisJobRepository
from app.domain.repositories.project_repository import ProjectRepository
from app.domain.repositories.source_file_repository import SourceFileRepository


class StartAnalysisUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        source_file_repository: SourceFileRepository,
        job_repository: AnalysisJobRepository,
    ) -> None:
        self._project_repository = project_repository
        self._source_file_repository = source_file_repository
        self._job_repository = job_repository

    async def execute(self, project_id: UUID) -> AnalysisJob:
        project = await self._project_repository.find_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        source_files = await self._source_file_repository.find_by_project(project_id)
        if not source_files:
            raise NoSourceFilesError(f"No source files found for project {project_id}")

        job = AnalysisJob(
            id=uuid4(),
            project_id=project_id,
            status=JobStatus.pending,
            created_at=datetime.now(timezone.utc),
        )
        return await self._job_repository.create(job)
