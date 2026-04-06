from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.project import Project
from app.domain.repositories.project_repository import ProjectRepository
from app.infrastructure.database.models import ProjectModel


class SQLAlchemyProjectRepository(ProjectRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_domain(self, model: ProjectModel) -> Project:
        return Project(
            id=model.id,
            name=model.name,
            description=model.description,
            s3_prefix=model.s3_prefix,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def create(self, project: Project) -> Project:
        model = ProjectModel(
            id=project.id,
            name=project.name,
            description=project.description,
            s3_prefix=project.s3_prefix,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_domain(model)

    async def find_by_id(self, project_id: UUID) -> Project | None:
        result = await self._session.execute(
            select(ProjectModel).where(ProjectModel.id == project_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def find_all(self, page: int, per_page: int) -> tuple[list[Project], int]:
        offset = (page - 1) * per_page
        result = await self._session.execute(
            select(ProjectModel).order_by(ProjectModel.created_at.desc()).offset(offset).limit(per_page)
        )
        models = result.scalars().all()
        count_result = await self._session.execute(select(func.count(ProjectModel.id)))
        total = count_result.scalar_one()
        return [self._to_domain(m) for m in models], total

    async def delete(self, project_id: UUID) -> bool:
        result = await self._session.execute(
            select(ProjectModel).where(ProjectModel.id == project_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return False
        await self._session.delete(model)
        await self._session.flush()
        return True
