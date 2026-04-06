from dataclasses import dataclass, field
from uuid import UUID

from app.domain.exceptions import AnalysisJobNotFoundError
from app.domain.repositories.analysis_job_repository import AnalysisJobRepository
from app.domain.repositories.dependency_edge_repository import DependencyEdgeRepository
from app.domain.repositories.source_file_repository import SourceFileRepository


@dataclass
class FlowNode:
    id: str
    file_path: str
    language: str | None
    children: list["FlowNode"] = field(default_factory=list)


@dataclass
class FlowDataResult:
    roots: list[FlowNode]


class GetFlowDataUseCase:
    def __init__(
        self,
        job_repository: AnalysisJobRepository,
        edge_repository: DependencyEdgeRepository,
        source_file_repository: SourceFileRepository,
    ) -> None:
        self._job_repository = job_repository
        self._edge_repository = edge_repository
        self._source_file_repository = source_file_repository

    async def execute(self, job_id: UUID) -> FlowDataResult:
        job = await self._job_repository.find_by_id(job_id)
        if job is None:
            raise AnalysisJobNotFoundError(f"Job {job_id} not found")

        edges = await self._edge_repository.find_by_job(job_id)
        source_files = await self._source_file_repository.find_by_project(job.project_id)

        file_map = {f.id: f for f in source_files}
        children_map: dict[UUID, list[UUID]] = {}
        has_parent: set[UUID] = set()

        for e in edges:
            children_map.setdefault(e.source_file_id, []).append(e.target_file_id)
            has_parent.add(e.target_file_id)

        def build_node(file_id: UUID, visited: set[UUID]) -> FlowNode | None:
            if file_id in visited or file_id not in file_map:
                return None
            visited.add(file_id)
            f = file_map[file_id]
            node = FlowNode(id=str(file_id), file_path=f.file_path, language=f.language)
            for child_id in children_map.get(file_id, []):
                child = build_node(child_id, visited)
                if child:
                    node.children.append(child)
            return node

        all_ids = set(children_map.keys()) | has_parent
        root_ids = all_ids - has_parent
        roots = []
        for rid in root_ids:
            node = build_node(rid, set())
            if node:
                roots.append(node)

        return FlowDataResult(roots=roots)
