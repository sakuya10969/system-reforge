from datetime import datetime, timezone
from uuid import uuid4

from app.domain.models.project import Project
from app.domain.repositories.project_repository import ProjectRepository


class CreateProjectUseCase:
    def __init__(self, repository: ProjectRepository) -> None:
        self._repository = repository

    async def execute(self, name: str, description: str | None = None) -> Project:
        if not name or not name.strip():
            raise ValueError("Project name must not be empty or whitespace only")
        if len(name) > 255:
            raise ValueError("Project name must not exceed 255 characters")

        project_id = uuid4()
        now = datetime.now(timezone.utc)
        project = Project(
            id=project_id,
            name=name.strip(),
            description=description,
            s3_prefix=f"projects/{project_id}",
            created_at=now,
            updated_at=now,
        )
        return await self._repository.create(project)
