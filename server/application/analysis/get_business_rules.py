from uuid import UUID

from server.domain.exceptions import AnalysisJobNotFoundError
from server.domain.models.business_rule import BusinessRule, RuleType
from server.domain.repositories.analysis_job_repository import AnalysisJobRepository
from server.domain.repositories.business_rule_repository import BusinessRuleRepository


class GetBusinessRulesUseCase:
    def __init__(
        self,
        job_repository: AnalysisJobRepository,
        business_rule_repository: BusinessRuleRepository,
    ) -> None:
        self._job_repository = job_repository
        self._business_rule_repository = business_rule_repository

    async def execute(self, job_id: UUID, rule_type: RuleType | None = None) -> list[BusinessRule]:
        job = await self._job_repository.find_by_id(job_id)
        if job is None:
            raise AnalysisJobNotFoundError(f"Job {job_id} not found")
        return await self._business_rule_repository.find_by_job(job_id, rule_type=rule_type)
