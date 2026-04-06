from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.dependency_edge import DependencyEdge, DependencyType
from app.domain.repositories.dependency_edge_repository import DependencyEdgeRepository
from app.infrastructure.database.models import DependencyEdgeModel


class SQLAlchemyDependencyEdgeRepository(DependencyEdgeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_domain(self, model: DependencyEdgeModel) -> DependencyEdge:
        return DependencyEdge(
            id=model.id,
            job_id=model.job_id,
            source_file_id=model.source_file_id,
            target_file_id=model.target_file_id,
            dependency_type=DependencyType(model.dependency_type),
            metadata=model.metadata_ or {},
        )

    async def find_by_job(self, job_id: UUID) -> list[DependencyEdge]:
        result = await self._session.execute(
            select(DependencyEdgeModel).where(DependencyEdgeModel.job_id == job_id)
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def create_many(self, edges: list[DependencyEdge]) -> list[DependencyEdge]:
        models = [
            DependencyEdgeModel(
                id=e.id,
                job_id=e.job_id,
                source_file_id=e.source_file_id,
                target_file_id=e.target_file_id,
                dependency_type=e.dependency_type.value,
                metadata_=e.metadata,
            )
            for e in edges
        ]
        self._session.add_all(models)
        await self._session.flush()
        return [self._to_domain(m) for m in models]
