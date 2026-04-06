from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.models.requirement import Requirement, RequirementPriority, RequirementStatus
from server.domain.repositories.requirement_repository import RequirementRepository
from server.infrastructure.database.models import RequirementModel


class SQLAlchemyRequirementRepository(RequirementRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_domain(self, model: RequirementModel) -> Requirement:
        return Requirement(
            id=model.id,
            job_id=model.job_id,
            title=model.title,
            description=model.description,
            category=model.category,
            priority=RequirementPriority(model.priority),
            status=RequirementStatus(model.status),
            source_rules=model.source_rules or [],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def find_by_job(self, job_id: UUID) -> list[Requirement]:
        result = await self._session.execute(
            select(RequirementModel)
            .where(RequirementModel.job_id == job_id)
            .order_by(RequirementModel.created_at.asc())
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def find_by_id(self, requirement_id: UUID) -> Requirement | None:
        result = await self._session.execute(
            select(RequirementModel).where(RequirementModel.id == requirement_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def update(self, requirement: Requirement) -> Requirement:
        result = await self._session.execute(
            select(RequirementModel).where(RequirementModel.id == requirement.id)
        )
        model = result.scalar_one()
        model.title = requirement.title
        model.description = requirement.description
        model.category = requirement.category
        model.priority = requirement.priority.value
        model.status = requirement.status.value
        model.source_rules = requirement.source_rules
        model.updated_at = requirement.updated_at
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def create_many(self, requirements: list[Requirement]) -> list[Requirement]:
        models = [
            RequirementModel(
                id=r.id,
                job_id=r.job_id,
                title=r.title,
                description=r.description,
                category=r.category,
                priority=r.priority.value,
                status=r.status.value,
                source_rules=r.source_rules,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in requirements
        ]
        self._session.add_all(models)
        await self._session.flush()
        return [self._to_domain(m) for m in models]
