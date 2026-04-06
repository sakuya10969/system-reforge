import { Badge, Center, Skeleton, Table, Text } from "@mantine/core";
import type { Job, JobStatus } from "~/entities/job";

const STATUS_COLOR: Record<JobStatus, string> = {
  pending: "gray",
  running: "blue",
  completed: "green",
  failed: "red",
};

const STATUS_LABEL: Record<JobStatus, string> = {
  pending: "待機中",
  running: "実行中",
  completed: "完了",
  failed: "失敗",
};

interface Props {
  jobs: Job[] | undefined;
  isLoading: boolean;
  onSelect?: (job: Job) => void;
}

export function JobListWidget({ jobs, isLoading, onSelect }: Props) {
  if (isLoading) return <Skeleton height={200} />;
  if (!jobs || jobs.length === 0) {
    return <Center py="xl"><Text c="dimmed">解析ジョブがありません</Text></Center>;
  }

  return (
    <Table striped highlightOnHover>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>ジョブID</Table.Th>
          <Table.Th>ステータス</Table.Th>
          <Table.Th>作成日時</Table.Th>
          <Table.Th>完了日時</Table.Th>
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {jobs.map((job) => (
          <Table.Tr
            key={job.id}
            onClick={() => onSelect?.(job)}
            style={{ cursor: onSelect ? "pointer" : "default" }}
          >
            <Table.Td><Text size="xs" ff="monospace">{job.id.slice(0, 8)}…</Text></Table.Td>
            <Table.Td>
              <Badge color={STATUS_COLOR[job.status]}>{STATUS_LABEL[job.status]}</Badge>
            </Table.Td>
            <Table.Td><Text size="sm">{new Date(job.created_at).toLocaleString("ja-JP")}</Text></Table.Td>
            <Table.Td>
              <Text size="sm">{job.completed_at ? new Date(job.completed_at).toLocaleString("ja-JP") : "—"}</Text>
            </Table.Td>
          </Table.Tr>
        ))}
      </Table.Tbody>
    </Table>
  );
}
