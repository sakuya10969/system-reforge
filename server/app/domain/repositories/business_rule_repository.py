from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.business_rule import BusinessRule, RuleType


class BusinessRuleRepository(ABC):
    @abstractmethod
    async def create_many(self, rules: list[BusinessRule]) -> list[BusinessRule]: ...

    @abstractmethod
    async def find_by_job(
        self, job_id: UUID, rule_type: RuleType | None = None
    ) -> list[BusinessRule]: ...
