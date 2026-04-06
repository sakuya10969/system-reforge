from uuid import UUID

from pydantic import BaseModel


class GraphNodeResponse(BaseModel):
    id: str
    file_path: str
    language: str | None


class GraphEdgeResponse(BaseModel):
    id: str
    source: str
    target: str
    dependency_type: str


class DependencyGraphData(BaseModel):
    nodes: list[GraphNodeResponse]
    edges: list[GraphEdgeResponse]


class DependencyGraphResponse(BaseModel):
    data: DependencyGraphData


class FlowNodeResponse(BaseModel):
    id: str
    file_path: str
    language: str | None
    children: list["FlowNodeResponse"] = []


class FlowDataData(BaseModel):
    roots: list[FlowNodeResponse]


class FlowDataResponse(BaseModel):
    data: FlowDataData


class SourceFileResponse(BaseModel):
    id: UUID
    project_id: UUID
    file_path: str
    language: str | None
    s3_key: str


class SourceFileListResponse(BaseModel):
    data: list[SourceFileResponse]
