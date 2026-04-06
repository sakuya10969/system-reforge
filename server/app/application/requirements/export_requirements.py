from uuid import UUID

from app.domain.exceptions import AnalysisJobNotFoundError
from app.domain.repositories.analysis_job_repository import AnalysisJobRepository
from app.domain.repositories.requirement_repository import RequirementRepository
from app.domain.services.markdown_exporter import MarkdownExporter


class ExportRequirementsUseCase:
    def __init__(
        self,
        job_repository: AnalysisJobRepository,
        requirement_repository: RequirementRepository,
        exporter: MarkdownExporter,
    ) -> None:
        self._job_repository = job_repository
        self._requirement_repository = requirement_repository
        self._exporter = exporter

    async def execute(self, job_id: UUID) -> str:
        job = await self._job_repository.find_by_id(job_id)
        if job is None:
            raise AnalysisJobNotFoundError(f"Job {job_id} not found")
        requirements = await self._requirement_repository.find_by_job(job_id)
        return self._exporter.to_markdown(requirements)
