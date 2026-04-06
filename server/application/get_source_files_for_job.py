from uuid import UUID

from server.domain.exceptions import AnalysisJobNotFoundError
from server.domain.models.source_file import SourceFile
from server.domain.repositories.analysis_job_repository import AnalysisJobRepository
from server.domain.repositories.source_file_repository import SourceFileRepository


class GetSourceFilesForJobUseCase:
    def __init__(
        self,
        job_repository: AnalysisJobRepository,
        source_file_repository: SourceFileRepository,
    ) -> None:
        self._job_repository = job_repository
        self._source_file_repository = source_file_repository

    async def execute(self, job_id: UUID) -> list[SourceFile]:
        job = await self._job_repository.find_by_id(job_id)
        if job is None:
            raise AnalysisJobNotFoundError(f"Job {job_id} not found")
        return await self._source_file_repository.find_by_project(job.project_id)
