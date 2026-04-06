from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from server.api.dependencies import (
    get_analysis_job_repository,
    get_business_rule_repository,
    get_dependency_edge_repository,
    get_meaning_extraction_service,
    get_requirement_repository,
    get_source_file_repository,
)
from server.api.schemas.analysis import (
    DependencyGraphData,
    DependencyGraphResponse,
    FlowDataData,
    FlowDataResponse,
    FlowNodeResponse,
    GraphEdgeResponse,
    GraphNodeResponse,
    SourceFileListResponse,
    SourceFileResponse,
)
from server.api.schemas.business_rule import (
    BusinessRuleListResponse,
    BusinessRuleResponse,
    SourceLocationSchema,
)
from server.api.schemas.requirement import ExportData, ExportResponse, RequirementListResponse, RequirementResponse, RequirementUpdateRequest
from server.application.analysis import (
    ExtractBusinessRulesUseCase,
    FlowNode,
    GetBusinessRulesUseCase,
    GetDependencyGraphUseCase,
    GetFlowDataUseCase,
    GetSourceFilesForJobUseCase,
)
from server.application.requirements import (
    ExportRequirementsUseCase,
    GetRequirementsUseCase,
    UpdateRequirementUseCase,
)
from server.domain.models.business_rule import RuleType
from server.domain.repositories.analysis_job_repository import AnalysisJobRepository
from server.domain.repositories.business_rule_repository import BusinessRuleRepository
from server.domain.repositories.dependency_edge_repository import DependencyEdgeRepository
from server.domain.repositories.requirement_repository import RequirementRepository
from server.domain.repositories.source_file_repository import SourceFileRepository
from server.domain.services.meaning_extraction_service import MeaningExtractionService
from server.domain.services.markdown_exporter import MarkdownExporter

router = APIRouter(prefix="/api/v1", tags=["analysis"])

JobRepoDep = Annotated[AnalysisJobRepository, Depends(get_analysis_job_repository)]
SourceRepoDep = Annotated[SourceFileRepository, Depends(get_source_file_repository)]
EdgeRepoDep = Annotated[DependencyEdgeRepository, Depends(get_dependency_edge_repository)]
RuleRepoDep = Annotated[BusinessRuleRepository, Depends(get_business_rule_repository)]
RequirementRepoDep = Annotated[RequirementRepository, Depends(get_requirement_repository)]
ExtractionServiceDep = Annotated[MeaningExtractionService, Depends(get_meaning_extraction_service)]


def _flow_node_to_response(node: FlowNode) -> FlowNodeResponse:
    return FlowNodeResponse(
        id=node.id,
        file_path=node.file_path,
        language=node.language,
        children=[_flow_node_to_response(c) for c in node.children],
    )


@router.get("/jobs/{job_id}/source-files")
async def get_source_files(
    job_id: UUID,
    job_repo: JobRepoDep,
    source_repo: SourceRepoDep,
) -> SourceFileListResponse:
    uc = GetSourceFilesForJobUseCase(job_repo, source_repo)
    files = await uc.execute(job_id)
    return SourceFileListResponse(
        data=[SourceFileResponse(
            id=f.id, project_id=f.project_id, file_path=f.file_path,
            language=f.language, s3_key=f.s3_key,
        ) for f in files]
    )


@router.get("/jobs/{job_id}/dependencies")
async def get_dependencies(
    job_id: UUID,
    job_repo: JobRepoDep,
    edge_repo: EdgeRepoDep,
    source_repo: SourceRepoDep,
) -> DependencyGraphResponse:
    uc = GetDependencyGraphUseCase(job_repo, edge_repo, source_repo)
    result = await uc.execute(job_id)
    return DependencyGraphResponse(
        data=DependencyGraphData(
            nodes=[GraphNodeResponse(id=n.id, file_path=n.file_path, language=n.language) for n in result.nodes],
            edges=[GraphEdgeResponse(id=e.id, source=e.source, target=e.target, dependency_type=e.dependency_type) for e in result.edges],
        )
    )


@router.get("/jobs/{job_id}/flow")
async def get_flow(
    job_id: UUID,
    job_repo: JobRepoDep,
    edge_repo: EdgeRepoDep,
    source_repo: SourceRepoDep,
) -> FlowDataResponse:
    uc = GetFlowDataUseCase(job_repo, edge_repo, source_repo)
    result = await uc.execute(job_id)
    return FlowDataResponse(
        data=FlowDataData(roots=[_flow_node_to_response(r) for r in result.roots])
    )


@router.get("/jobs/{job_id}/business-rules")
async def get_business_rules(
    job_id: UUID,
    job_repo: JobRepoDep,
    rule_repo: RuleRepoDep,
    rule_type: str | None = Query(default=None),
) -> BusinessRuleListResponse:
    rt = RuleType(rule_type) if rule_type else None
    uc = GetBusinessRulesUseCase(job_repo, rule_repo)
    rules = await uc.execute(job_id, rule_type=rt)
    return BusinessRuleListResponse(
        data=[BusinessRuleResponse(
            id=r.id,
            job_id=r.job_id,
            source_file_id=r.source_file_id,
            rule_type=r.rule_type.value,
            description=r.description,
            source_location=SourceLocationSchema(
                file_path=r.source_location.file_path,
                start_line=r.source_location.start_line,
                end_line=r.source_location.end_line,
            ) if r.source_location else None,
            created_at=r.created_at,
        ) for r in rules]
    )


@router.get("/jobs/{job_id}/requirements")
async def get_requirements(
    job_id: UUID,
    job_repo: JobRepoDep,
    req_repo: RequirementRepoDep,
) -> RequirementListResponse:
    uc = GetRequirementsUseCase(job_repo, req_repo)
    reqs = await uc.execute(job_id)
    return RequirementListResponse(
        data=[RequirementResponse(
            id=r.id, job_id=r.job_id, title=r.title, description=r.description,
            category=r.category, priority=r.priority.value, status=r.status.value,
            source_rules=r.source_rules, created_at=r.created_at, updated_at=r.updated_at,
        ) for r in reqs]
    )


@router.put("/requirements/{requirement_id}")
async def update_requirement(
    requirement_id: UUID,
    body: RequirementUpdateRequest,
    req_repo: RequirementRepoDep,
) -> dict:
    uc = UpdateRequirementUseCase(req_repo)
    req = await uc.execute(
        requirement_id=requirement_id,
        title=body.title,
        description=body.description,
        category=body.category,
        priority=body.priority,
        status=body.status,
    )
    return {"data": RequirementResponse(
        id=req.id, job_id=req.job_id, title=req.title, description=req.description,
        category=req.category, priority=req.priority.value, status=req.status.value,
        source_rules=req.source_rules, created_at=req.created_at, updated_at=req.updated_at,
    )}


@router.post("/jobs/{job_id}/requirements/export")
async def export_requirements(
    job_id: UUID,
    job_repo: JobRepoDep,
    req_repo: RequirementRepoDep,
) -> ExportResponse:
    uc = ExportRequirementsUseCase(job_repo, req_repo, MarkdownExporter())
    markdown = await uc.execute(job_id)
    return ExportResponse(data=ExportData(markdown=markdown))
