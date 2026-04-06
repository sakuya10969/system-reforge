from uuid import UUID

from server.domain.exceptions import AnalysisJobNotFoundError
from server.domain.models.requirement import Requirement
from server.domain.repositories.analysis_job_repository import AnalysisJobRepository
from server.domain.repositories.requirement_repository import RequirementRepository


class GetRequirementsUseCase:
    def __init__(
        self,
        job_repository: AnalysisJobRepository,
        requirement_repository: RequirementRepository,
    ) -> None:
        self._job_repository = job_repository
        self._requirement_repository = requirement_repository

    async def execute(self, job_id: UUID) -> list[Requirement]:
        job = await self._job_repository.find_by_id(job_id)
        if job is None:
            raise AnalysisJobNotFoundError(f"Job {job_id} not found")
        return await self._requirement_repository.find_by_job(job_id)
