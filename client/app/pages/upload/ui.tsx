import { Button, Container, Group, Title } from "@mantine/core";
import { Link, useParams } from "react-router";
import { UploadDropzone } from "~/features/upload-zip";

export function UploadPage() {
  const { projectId } = useParams<{ projectId: string }>();

  return (
    <Container size="sm" py="xl">
      <Group justify="space-between" mb="lg">
        <Title order={2}>ソースコードアップロード</Title>
        <Button variant="subtle" component={Link} to="/projects">← 一覧に戻る</Button>
      </Group>
      {projectId && <UploadDropzone projectId={projectId} onSuccess={() => {}} />}
    </Container>
  );
}
