from uuid import UUID

from server.domain.services.analysis_service import AnalysisService


class StubAnalysisService(AnalysisService):
    async def analyze(self, job_id: UUID, project_id: UUID) -> None:
        pass
