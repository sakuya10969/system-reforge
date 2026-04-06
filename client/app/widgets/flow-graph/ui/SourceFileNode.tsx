import { Badge, Card, Text } from "@mantine/core";
import { Handle, Position } from "@xyflow/react";

interface Props {
  data: { file_path: string; language: string | null };
}

export function SourceFileNode({ data }: Props) {
  const fileName = data.file_path.split("/").pop() ?? data.file_path;
  return (
    <>
      <Handle type="target" position={Position.Top} />
      <Card shadow="xs" padding="xs" radius="sm" withBorder style={{ minWidth: 160 }}>
        <Text size="xs" fw={500} truncate="end" title={data.file_path}>{fileName}</Text>
        {data.language && <Badge size="xs" variant="light" mt={4}>{data.language}</Badge>}
      </Card>
      <Handle type="source" position={Position.Bottom} />
    </>
  );
}
