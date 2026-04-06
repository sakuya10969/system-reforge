from uuid import UUID

from app.domain.exceptions import AnalysisJobNotFoundError
from app.domain.models.analysis_job import AnalysisJob
from app.domain.repositories.analysis_job_repository import AnalysisJobRepository


class GetJobUseCase:
    def __init__(self, repository: AnalysisJobRepository) -> None:
        self._repository = repository

    async def execute(self, job_id: UUID) -> AnalysisJob:
        job = await self._repository.find_by_id(job_id)
        if job is None:
            raise AnalysisJobNotFoundError(f"Job {job_id} not found")
        return job
