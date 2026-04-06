from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from server.api.dependencies import (
    get_project_repository,
    get_s3_client,
    get_source_file_repository,
)
from server.api.schemas.upload import UploadResultData, UploadResultResponse, UploadedFileResponse
from server.application.upload_source import UploadSourceUseCase
from server.domain.repositories.project_repository import ProjectRepository
from server.domain.repositories.source_file_repository import SourceFileRepository
from server.infrastructure.storage.s3_client import S3Client

router = APIRouter(prefix="/api/v1/projects", tags=["upload"])

ProjectRepoDep = Annotated[ProjectRepository, Depends(get_project_repository)]
SourceRepoDep = Annotated[SourceFileRepository, Depends(get_source_file_repository)]
S3Dep = Annotated[S3Client, Depends(get_s3_client)]


@router.post("/{project_id}/upload")
async def upload_zip(
    project_id: UUID,
    file: UploadFile,
    project_repo: ProjectRepoDep,
    source_repo: SourceRepoDep,
    s3_client: S3Dep,
) -> UploadResultResponse:
    allowed_types = {"application/zip", "application/x-zip-compressed", "application/octet-stream"}
    if file.content_type not in allowed_types and not (file.filename or "").endswith(".zip"):
        raise HTTPException(status_code=422, detail="File must be a ZIP archive")

    content = await file.read()
    uc = UploadSourceUseCase(project_repo, source_repo, s3_client)
    result = await uc.execute(project_id, content)

    return UploadResultResponse(
        data=UploadResultData(
            project_id=result.project_id,
            total_files=result.total_files,
            uploaded_files=[
                UploadedFileResponse(
                    file_path=f.file_path,
                    language=f.language,
                    s3_key=f.s3_key,
                )
                for f in result.uploaded_files
            ],
        )
    )
