from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.business_rule import BusinessRule, RuleType, SourceLocation
from app.domain.repositories.business_rule_repository import BusinessRuleRepository
from app.infrastructure.database.models import BusinessRuleModel


class SQLAlchemyBusinessRuleRepository(BusinessRuleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_domain(self, model: BusinessRuleModel) -> BusinessRule:
        source_location = None
        if model.source_location:
            source_location = SourceLocation(
                file_path=model.source_location.get("file_path", ""),
                start_line=model.source_location.get("start_line"),
                end_line=model.source_location.get("end_line"),
            )
        return BusinessRule(
            id=model.id,
            job_id=model.job_id,
            source_file_id=model.source_file_id,
            rule_type=RuleType(model.rule_type),
            description=model.description,
            source_location=source_location,
            created_at=model.created_at,
        )

    async def create_many(self, rules: list[BusinessRule]) -> list[BusinessRule]:
        models = [
            BusinessRuleModel(
                id=r.id,
                job_id=r.job_id,
                source_file_id=r.source_file_id,
                rule_type=r.rule_type.value,
                description=r.description,
                source_location={
                    "file_path": r.source_location.file_path,
                    "start_line": r.source_location.start_line,
                    "end_line": r.source_location.end_line,
                } if r.source_location else None,
                created_at=r.created_at,
            )
            for r in rules
        ]
        self._session.add_all(models)
        await self._session.flush()
        return [self._to_domain(m) for m in models]

    async def find_by_job(self, job_id: UUID, rule_type: RuleType | None = None) -> list[BusinessRule]:
        query = select(BusinessRuleModel).where(BusinessRuleModel.job_id == job_id).order_by(BusinessRuleModel.created_at.asc())
        if rule_type is not None:
            query = query.where(BusinessRuleModel.rule_type == rule_type.value)
        result = await self._session.execute(query)
        return [self._to_domain(m) for m in result.scalars().all()]
