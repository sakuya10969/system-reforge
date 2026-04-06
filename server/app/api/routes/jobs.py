from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from app.api.dependencies import (
    get_analysis_job_repository,
    get_analysis_service,
    get_project_repository,
    get_source_file_repository,
)
from app.api.schemas.job import JobCreateResponse, JobListResponse, JobResponse
from app.application.jobs import (
    GetJobUseCase,
    ListJobsUseCase,
    RunAnalysisUseCase,
    StartAnalysisUseCase,
)
from app.domain.repositories.analysis_job_repository import AnalysisJobRepository
from app.domain.repositories.project_repository import ProjectRepository
from app.domain.repositories.source_file_repository import SourceFileRepository
from app.domain.services.analysis_service import AnalysisService

router = APIRouter(tags=["jobs"])

ProjectRepoDep = Annotated[ProjectRepository, Depends(get_project_repository)]
SourceRepoDep = Annotated[SourceFileRepository, Depends(get_source_file_repository)]
JobRepoDep = Annotated[AnalysisJobRepository, Depends(get_analysis_job_repository)]
AnalysisServiceDep = Annotated[AnalysisService, Depends(get_analysis_service)]


@router.post("/api/v1/projects/{project_id}/jobs", status_code=201)
async def create_job(
    project_id: UUID,
    background_tasks: BackgroundTasks,
    project_repo: ProjectRepoDep,
    source_repo: SourceRepoDep,
    job_repo: JobRepoDep,
    analysis_service: AnalysisServiceDep,
) -> JobCreateResponse:
    uc = StartAnalysisUseCase(project_repo, source_repo, job_repo)
    job = await uc.execute(project_id)

    run_uc = RunAnalysisUseCase(job_repo, analysis_service)
    background_tasks.add_task(run_uc.execute, job.id)

    return JobCreateResponse(data=JobResponse.model_validate(job.__dict__))


@router.get("/api/v1/projects/{project_id}/jobs")
async def list_jobs(
    project_id: UUID,
    project_repo: ProjectRepoDep,
    job_repo: JobRepoDep,
) -> JobListResponse:
    uc = ListJobsUseCase(project_repo, job_repo)
    jobs = await uc.execute(project_id)
    return JobListResponse(data=[JobResponse.model_validate(j.__dict__) for j in jobs])


@router.get("/api/v1/jobs/{job_id}")
async def get_job(job_id: UUID, job_repo: JobRepoDep) -> dict:
    uc = GetJobUseCase(job_repo)
    job = await uc.execute(job_id)
    return {"data": JobResponse.model_validate(job.__dict__)}
