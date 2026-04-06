from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from server.application.sources.zip_extractor import extract_zip
from server.domain.exceptions import ProjectNotFoundError
from server.domain.models.source_file import SourceFile
from server.domain.repositories.project_repository import ProjectRepository
from server.domain.repositories.source_file_repository import SourceFileRepository
from server.domain.services.storage_client import StorageClient


@dataclass
class UploadedFileInfo:
    file_path: str
    language: str | None
    s3_key: str


@dataclass
class UploadResult:
    project_id: UUID
    uploaded_files: list[UploadedFileInfo]
    total_files: int


class UploadSourceUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        source_file_repository: SourceFileRepository,
        storage_client: StorageClient,
    ) -> None:
        self._project_repository = project_repository
        self._source_file_repository = source_file_repository
        self._storage_client = storage_client

    async def execute(self, project_id: UUID, zip_data: bytes) -> UploadResult:
        project = await self._project_repository.find_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")

        extracted = extract_zip(zip_data)
        now = datetime.now(timezone.utc)
        source_files: list[SourceFile] = []

        for ef in extracted:
            s3_key = self._storage_client.generate_source_key(project.s3_prefix, ef.file_path)
            self._storage_client.upload_file(s3_key, ef.content)
            source_files.append(SourceFile(
                id=uuid4(),
                project_id=project_id,
                file_path=ef.file_path,
                language=ef.language,
                s3_key=s3_key,
                created_at=now,
            ))

        saved = await self._source_file_repository.create_many(source_files)
        uploaded_files = [
            UploadedFileInfo(file_path=f.file_path, language=f.language, s3_key=f.s3_key)
            for f in saved
        ]
        return UploadResult(
            project_id=project_id,
            uploaded_files=uploaded_files,
            total_files=len(saved),
        )
