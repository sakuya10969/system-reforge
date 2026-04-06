from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.domain.models.source_file import SourceFile
from server.domain.repositories.source_file_repository import SourceFileRepository
from server.infrastructure.database.models import SourceFileModel


class SQLAlchemySourceFileRepository(SourceFileRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_domain(self, model: SourceFileModel) -> SourceFile:
        return SourceFile(
            id=model.id,
            project_id=model.project_id,
            file_path=model.file_path,
            language=model.language,
            s3_key=model.s3_key,
            created_at=model.created_at,
        )

    async def create_many(self, files: list[SourceFile]) -> list[SourceFile]:
        models = [
            SourceFileModel(
                id=f.id,
                project_id=f.project_id,
                file_path=f.file_path,
                language=f.language,
                s3_key=f.s3_key,
                created_at=f.created_at,
            )
            for f in files
        ]
        self._session.add_all(models)
        await self._session.flush()
        return [self._to_domain(m) for m in models]

    async def find_by_project(self, project_id: UUID) -> list[SourceFile]:
        result = await self._session.execute(
            select(SourceFileModel).where(SourceFileModel.project_id == project_id)
        )
        return [self._to_domain(m) for m in result.scalars().all()]

    async def find_by_id(self, file_id: UUID) -> SourceFile | None:
        result = await self._session.execute(
            select(SourceFileModel).where(SourceFileModel.id == file_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
