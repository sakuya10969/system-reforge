from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions import AnalysisJobNotFoundError
from app.domain.models.business_rule import BusinessRule, RuleType, SourceLocation
from app.domain.repositories.analysis_job_repository import AnalysisJobRepository
from app.domain.repositories.business_rule_repository import BusinessRuleRepository
from app.domain.repositories.source_file_repository import SourceFileRepository
from app.domain.services.meaning_extraction_service import IntermediateData, MeaningExtractionService


class ExtractBusinessRulesUseCase:
    def __init__(
        self,
        job_repository: AnalysisJobRepository,
        source_file_repository: SourceFileRepository,
        business_rule_repository: BusinessRuleRepository,
        extraction_service: MeaningExtractionService,
    ) -> None:
        self._job_repository = job_repository
        self._source_file_repository = source_file_repository
        self._business_rule_repository = business_rule_repository
        self._extraction_service = extraction_service

    async def execute(self, job_id: UUID) -> list[BusinessRule]:
        job = await self._job_repository.find_by_id(job_id)
        if job is None:
            raise AnalysisJobNotFoundError(f"Job {job_id} not found")

        source_files = await self._source_file_repository.find_by_project(job.project_id)
        data_list = [
            IntermediateData(file_path=f.file_path, content="", language=f.language)
            for f in source_files
        ]

        extracted = await self._extraction_service.extract(data_list)
        file_path_map = {f.file_path: f for f in source_files}
        now = datetime.now(timezone.utc)

        rules: list[BusinessRule] = []
        for er in extracted:
            if not er.description.strip():
                continue
            source_file = file_path_map.get(er.source_file_path or "")
            rules.append(BusinessRule(
                id=uuid4(),
                job_id=job_id,
                source_file_id=source_file.id if source_file else None,
                rule_type=RuleType(er.rule_type),
                description=er.description,
                source_location=SourceLocation(
                    file_path=er.source_file_path or "",
                    start_line=er.start_line,
                    end_line=er.end_line,
                ) if er.source_file_path else None,
                created_at=now,
            ))

        return await self._business_rule_repository.create_many(rules)
