import "@xyflow/react/dist/style.css";

import { Button, Center, Checkbox, Group, Stack, Text } from "@mantine/core";
import { Background, Controls, ReactFlow, useEdgesState, useNodesState, type Node, type Edge } from "@xyflow/react";
import { useEffect, useMemo, useState } from "react";
import type { DependencyGraph, DependencyType } from "~/entities/dependency";
import { filterEdgesByType } from "../lib/filter";
import { applyDagreLayout, toReactFlowEdges, toReactFlowNodes } from "../lib/transform";
import { SourceFileNode } from "./SourceFileNode";

const nodeTypes = { sourceFile: SourceFileNode };

const ALL_TYPES: DependencyType[] = ["CALL", "COPY", "INCLUDE"];

interface Props {
  graph: DependencyGraph | undefined;
  isLoading: boolean;
}

export function FlowGraph({ graph, isLoading }: Props) {
  const [activeTypes, setActiveTypes] = useState<DependencyType[]>(ALL_TYPES);
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  const filteredEdges = useMemo(
    () => filterEdgesByType(graph?.edges ?? [], activeTypes),
    [graph?.edges, activeTypes],
  );

  const applyLayout = () => {
    if (!graph) return;
    const rfNodes = toReactFlowNodes(graph.nodes);
    const rfEdges = toReactFlowEdges(filteredEdges);
    const laid = applyDagreLayout(rfNodes, rfEdges);
    setNodes(laid);
    setEdges(rfEdges);
  };

  useEffect(applyLayout, [graph, filteredEdges]);

  const toggleType = (type: DependencyType) => {
    setActiveTypes((prev) =>
      prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type],
    );
  };

  if (isLoading) return <Center h={400}><Text c="dimmed">読み込み中...</Text></Center>;
  if (!graph || graph.nodes.length === 0) {
    return <Center h={400}><Text c="dimmed">依存関係データがありません</Text></Center>;
  }

  return (
    <Stack>
      <Group>
        {ALL_TYPES.map((t) => (
          <Checkbox
            key={t}
            label={t}
            checked={activeTypes.includes(t)}
            onChange={() => toggleType(t)}
          />
        ))}
        <Button size="xs" variant="subtle" onClick={applyLayout}>レイアウトリセット</Button>
      </Group>
      <div style={{ height: 600, border: "1px solid #dee2e6", borderRadius: 8 }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
    </Stack>
  );
}
