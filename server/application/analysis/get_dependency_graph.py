from dataclasses import dataclass
from uuid import UUID

from server.domain.exceptions import AnalysisJobNotFoundError
from server.domain.models.dependency_edge import DependencyType
from server.domain.repositories.analysis_job_repository import AnalysisJobRepository
from server.domain.repositories.dependency_edge_repository import DependencyEdgeRepository
from server.domain.repositories.source_file_repository import SourceFileRepository


@dataclass
class GraphNode:
    id: str
    file_path: str
    language: str | None


@dataclass
class GraphEdge:
    id: str
    source: str
    target: str
    dependency_type: str


@dataclass
class DependencyGraphResult:
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class GetDependencyGraphUseCase:
    def __init__(
        self,
        job_repository: AnalysisJobRepository,
        edge_repository: DependencyEdgeRepository,
        source_file_repository: SourceFileRepository,
    ) -> None:
        self._job_repository = job_repository
        self._edge_repository = edge_repository
        self._source_file_repository = source_file_repository

    async def execute(self, job_id: UUID) -> DependencyGraphResult:
        job = await self._job_repository.find_by_id(job_id)
        if job is None:
            raise AnalysisJobNotFoundError(f"Job {job_id} not found")

        edges = await self._edge_repository.find_by_job(job_id)
        source_files = await self._source_file_repository.find_by_project(job.project_id)

        file_map = {f.id: f for f in source_files}
        involved_ids = set()
        for e in edges:
            involved_ids.add(e.source_file_id)
            involved_ids.add(e.target_file_id)

        nodes = [
            GraphNode(id=str(f.id), file_path=f.file_path, language=f.language)
            for f in source_files if f.id in involved_ids
        ]
        graph_edges = [
            GraphEdge(
                id=str(e.id),
                source=str(e.source_file_id),
                target=str(e.target_file_id),
                dependency_type=e.dependency_type.value,
            )
            for e in edges
        ]
        return DependencyGraphResult(nodes=nodes, edges=graph_edges)
