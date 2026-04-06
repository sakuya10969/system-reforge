from datetime import datetime, timezone
from uuid import UUID

from server.domain.models.analysis_job import JobStatus
from server.domain.repositories.analysis_job_repository import AnalysisJobRepository
from server.domain.services.analysis_service import AnalysisService


class RunAnalysisUseCase:
    def __init__(
        self,
        job_repository: AnalysisJobRepository,
        analysis_service: AnalysisService,
    ) -> None:
        self._job_repository = job_repository
        self._analysis_service = analysis_service

    async def execute(self, job_id: UUID) -> None:
        job = await self._job_repository.find_by_id(job_id)
        if job is None:
            return

        now = datetime.now(timezone.utc)
        job.transition_to(JobStatus.running, started_at=now)
        await self._job_repository.update(job)

        try:
            await self._analysis_service.analyze(job.id, job.project_id)
            job.transition_to(JobStatus.completed, completed_at=datetime.now(timezone.utc))
        except Exception as e:
            job.transition_to(JobStatus.failed, error_message=str(e), completed_at=datetime.now(timezone.utc))
        finally:
            await self._job_repository.update(job)
