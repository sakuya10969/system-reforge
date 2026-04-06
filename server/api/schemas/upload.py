from uuid import UUID

from pydantic import BaseModel


class UploadedFileResponse(BaseModel):
    file_path: str
    language: str | None
    s3_key: str


class UploadResultResponse(BaseModel):
    data: "UploadResultData"


class UploadResultData(BaseModel):
    project_id: UUID
    total_files: int
    uploaded_files: list[UploadedFileResponse]
