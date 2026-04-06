import { Alert, Button, Container, Group, Tabs, Title } from "@mantine/core";
import { Link, useParams } from "react-router";
import { useBusinessRules } from "~/entities/business-rule";
import { useJobs } from "~/entities/job";
import { useRequirements } from "~/entities/requirement";
import { StartAnalysisButton } from "~/features/start-analysis";
import { ExportButton } from "~/features/export-requirements";
import { JobListWidget } from "~/widgets/job-list";
import { RuleTable } from "~/widgets/rule-table";
import { RequirementsSection } from "./ui/RequirementsSection";

export async function loader() {
  return null;
}

export default function AnalysisPage() {
  const { projectId } = useParams<{ projectId: string }>();
  const { data: jobs, isLoading: jobsLoading, isError: jobsError } = useJobs(projectId ?? "");

  const latestJob = jobs?.[0];
  const latestJobId = latestJob?.id ?? "";

  const { data: rules, isLoading: rulesLoading } = useBusinessRules(latestJobId);
  const { data: requirements, isLoading: reqLoading } = useRequirements(latestJobId);

  return (
    <Container py="xl">
      <Group justify="space-between" mb="lg">
        <Title order={2}>解析管理</Title>
        <Group>
          <Button variant="subtle" component={Link} to="/projects">← 一覧</Button>
          <Button variant="light" component={Link} to={`/projects/${projectId}/upload`}>ソース管理</Button>
          {projectId && <StartAnalysisButton projectId={projectId} />}
        </Group>
      </Group>

      {jobsError && <Alert color="red" mb="md">ジョブ情報の取得に失敗しました</Alert>}

      <Tabs defaultValue="jobs">
        <Tabs.List mb="md">
          <Tabs.Tab value="jobs">ジョブ一覧</Tabs.Tab>
          <Tabs.Tab value="rules" disabled={!latestJobId}>業務ルール</Tabs.Tab>
          <Tabs.Tab value="requirements" disabled={!latestJobId}>要件レビュー</Tabs.Tab>
          <Tabs.Tab value="dependencies" disabled={!latestJobId}>依存関係</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="jobs">
          <JobListWidget jobs={jobs} isLoading={jobsLoading} />
        </Tabs.Panel>

        <Tabs.Panel value="rules">
          <RuleTable rules={rules} isLoading={rulesLoading} />
        </Tabs.Panel>

        <Tabs.Panel value="requirements">
          <Group justify="flex-end" mb="md">
            {latestJobId && <ExportButton jobId={latestJobId} />}
          </Group>
          <RequirementsSection requirements={requirements} isLoading={reqLoading} jobId={latestJobId} />
        </Tabs.Panel>

        <Tabs.Panel value="dependencies">
          <Button component={Link} to={`/jobs/${latestJobId}/dependencies`} variant="light" disabled={!latestJobId}>
            依存関係グラフを表示
          </Button>
        </Tabs.Panel>
      </Tabs>
    </Container>
  );
}
