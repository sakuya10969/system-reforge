from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Settings, get_settings
from app.domain.repositories.analysis_job_repository import AnalysisJobRepository
from app.domain.repositories.business_rule_repository import BusinessRuleRepository
from app.domain.repositories.dependency_edge_repository import DependencyEdgeRepository
from app.domain.repositories.project_repository import ProjectRepository
from app.domain.repositories.requirement_repository import RequirementRepository
from app.domain.repositories.source_file_repository import SourceFileRepository
from app.domain.services.analysis_service import AnalysisService
from app.domain.services.llm_client import LLMClient
from app.domain.services.meaning_extraction_service import MeaningExtractionService
from app.domain.services.storage_client import StorageClient
from app.infrastructure.analysis.stub_analysis_service import StubAnalysisService
from app.infrastructure.database.connection import get_session
from app.infrastructure.database.repositories.analysis_job_repository import SQLAlchemyAnalysisJobRepository
from app.infrastructure.database.repositories.business_rule_repository import SQLAlchemyBusinessRuleRepository
from app.infrastructure.database.repositories.dependency_edge_repository import SQLAlchemyDependencyEdgeRepository
from app.infrastructure.database.repositories.project_repository import SQLAlchemyProjectRepository
from app.infrastructure.database.repositories.requirement_repository import SQLAlchemyRequirementRepository
from app.infrastructure.database.repositories.source_file_repository import SQLAlchemySourceFileRepository
from app.infrastructure.llm.llm_client import BedrockLLMClient, StubLLMClient
from app.infrastructure.llm.meaning_extraction_service import DefaultMeaningExtractionService
from app.infrastructure.storage.s3_client import S3Client

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_project_repository(session: SessionDep) -> ProjectRepository:
    return SQLAlchemyProjectRepository(session)


def get_source_file_repository(session: SessionDep) -> SourceFileRepository:
    return SQLAlchemySourceFileRepository(session)


def get_analysis_job_repository(session: SessionDep) -> AnalysisJobRepository:
    return SQLAlchemyAnalysisJobRepository(session)


def get_dependency_edge_repository(session: SessionDep) -> DependencyEdgeRepository:
    return SQLAlchemyDependencyEdgeRepository(session)


def get_business_rule_repository(session: SessionDep) -> BusinessRuleRepository:
    return SQLAlchemyBusinessRuleRepository(session)


def get_requirement_repository(session: SessionDep) -> RequirementRepository:
    return SQLAlchemyRequirementRepository(session)


def get_analysis_service() -> AnalysisService:
    return StubAnalysisService()


def get_app_settings() -> Settings:
    return get_settings()


def get_llm_client() -> LLMClient:
    settings = get_settings()
    if settings.use_bedrock:
        return BedrockLLMClient(settings)
    return StubLLMClient()


def get_meaning_extraction_service(
    llm_client: Annotated[LLMClient, Depends(get_llm_client)],
) -> MeaningExtractionService:
    return DefaultMeaningExtractionService(llm_client)


def get_s3_client() -> StorageClient:
    return S3Client(get_settings())
