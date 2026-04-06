import type { GraphEdge } from "~/entities/dependency";
import type { DependencyType } from "~/entities/dependency";

export function filterEdgesByType(edges: GraphEdge[], types: DependencyType[]): GraphEdge[] {
  if (types.length === 0) return edges;
  return edges.filter((e) => types.includes(e.dependency_type));
}
