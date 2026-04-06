from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from server.api.dependencies import get_project_repository
from server.api.schemas.project import (
    PaginationResponse,
    ProjectCreateRequest,
    ProjectListResponse,
    ProjectResponse,
)
from server.application.create_project import CreateProjectUseCase
from server.application.delete_project import DeleteProjectUseCase
from server.application.get_project import GetProjectUseCase
from server.application.list_projects import ListProjectsUseCase
from server.domain.repositories.project_repository import ProjectRepository

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])

ProjectRepoDep = Annotated[ProjectRepository, Depends(get_project_repository)]


@router.post("", status_code=201)
async def create_project(body: ProjectCreateRequest, repo: ProjectRepoDep) -> dict:
    uc = CreateProjectUseCase(repo)
    project = await uc.execute(name=body.name, description=body.description)
    return {"data": ProjectResponse.model_validate(project.__dict__)}


@router.get("")
async def list_projects(
    repo: ProjectRepoDep,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
) -> ProjectListResponse:
    uc = ListProjectsUseCase(repo)
    projects, total = await uc.execute(page=page, per_page=per_page)
    return ProjectListResponse(
        data=[ProjectResponse.model_validate(p.__dict__) for p in projects],
        pagination=PaginationResponse(total=total, page=page, per_page=per_page),
    )


@router.get("/{project_id}")
async def get_project(project_id: UUID, repo: ProjectRepoDep) -> dict:
    uc = GetProjectUseCase(repo)
    project = await uc.execute(project_id)
    return {"data": ProjectResponse.model_validate(project.__dict__)}


@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: UUID, repo: ProjectRepoDep) -> None:
    uc = DeleteProjectUseCase(repo)
    await uc.execute(project_id)
