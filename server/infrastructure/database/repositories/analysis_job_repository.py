from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.models.analysis_job import AnalysisJob, JobStatus
from server.domain.repositories.analysis_job_repository import AnalysisJobRepository
from server.infrastructure.database.models import AnalysisJobModel


class SQLAlchemyAnalysisJobRepository(AnalysisJobRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_domain(self, model: AnalysisJobModel) -> AnalysisJob:
        return AnalysisJob(
            id=model.id,
            project_id=model.project_id,
            status=JobStatus(model.status),
            created_at=model.created_at,
            started_at=model.started_at,
            completed_at=model.completed_at,
            error_message=model.error_message,
        )

    async def create(self, job: AnalysisJob) -> AnalysisJob:
        model = AnalysisJobModel(
            id=job.id,
            project_id=job.project_id,
            status=job.status.value,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
            error_message=job.error_message,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def find_by_id(self, job_id: UUID) -> AnalysisJob | None:
        result = await self._session.execute(
            select(AnalysisJobModel).where(AnalysisJobModel.id == job_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def find_by_project(self, project_id: UUID) -> list[AnalysisJob]:
        result = await self._session.execute(
            select(AnalysisJobModel)
            .where(AnalysisJobModel.project_id == project_id)
            .order_by(AnalysisJobModel.created_at.desc())
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def update(self, job: AnalysisJob) -> AnalysisJob:
        result = await self._session.execute(
            select(AnalysisJobModel).where(AnalysisJobModel.id == job.id)
        )
        model = result.scalar_one()
        model.status = job.status.value
        model.started_at = job.started_at
        model.completed_at = job.completed_at
        model.error_message = job.error_message
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_domain(model)
