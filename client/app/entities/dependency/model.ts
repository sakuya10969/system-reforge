export type DependencyType = "CALL" | "COPY" | "INCLUDE";

export interface GraphNode {
  id: string;
  file_path: string;
  language: string | null;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  dependency_type: DependencyType;
}

export interface DependencyGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface FlowNode {
  id: string;
  file_path: string;
  language: string | null;
  children: FlowNode[];
}

export interface FlowData {
  roots: FlowNode[];
}
