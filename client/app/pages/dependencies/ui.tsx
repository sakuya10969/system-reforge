import { Alert, Button, Container, Group, Title } from "@mantine/core";
import { Link, useParams } from "react-router";
import { useDependencyGraph } from "~/entities/dependency";
import { FlowGraph } from "~/widgets/flow-graph";

export function DependenciesPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const { data, isLoading, isError } = useDependencyGraph(jobId ?? "");

  return (
    <Container size="xl" py="xl">
      <Group justify="space-between" mb="lg">
        <Title order={2}>依存関係グラフ</Title>
        <Button variant="subtle" component={Link} to="/projects">← 一覧</Button>
      </Group>

      {isError && <Alert color="red" mb="md">依存関係データの取得に失敗しました</Alert>}

      <FlowGraph graph={data} isLoading={isLoading} />
    </Container>
  );
}
