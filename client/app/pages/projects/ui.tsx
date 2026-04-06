import { ActionIcon, Alert, Button, Center, Group, Modal, Table, Text, Title } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { modals } from "@mantine/modals";
import { notifications } from "@mantine/notifications";
import { Link } from "react-router";
import { useDeleteProject, useProjects } from "~/entities/project";
import { CreateProjectForm } from "~/features/create-project";

export async function loader() {
  return null;
}

export default function ProjectsPage() {
  const { data, isLoading, isError } = useProjects();
  const { mutateAsync: deleteProject } = useDeleteProject();
  const [opened, { open, close }] = useDisclosure(false);

  const handleDelete = (id: string, name: string) => {
    modals.openConfirmModal({
      title: "プロジェクト削除",
      children: <Text>「{name}」を削除しますか？この操作は取り消せません。</Text>,
      labels: { confirm: "削除", cancel: "キャンセル" },
      confirmProps: { color: "red" },
      onConfirm: async () => {
        try {
          await deleteProject(id);
          notifications.show({ title: "削除完了", message: "プロジェクトを削除しました", color: "green" });
        } catch {
          notifications.show({ title: "エラー", message: "削除に失敗しました", color: "red" });
        }
      },
    });
  };

  return (
    <>
      <Group justify="space-between" mb="lg">
        <Title order={2}>プロジェクト一覧</Title>
        <Button onClick={open}>新規作成</Button>
      </Group>

      {isError && <Alert color="red" mb="md">プロジェクトの取得に失敗しました</Alert>}

      {isLoading ? (
        <Text c="dimmed">読み込み中...</Text>
      ) : !data?.data.length ? (
        <Center py="xl"><Text c="dimmed">プロジェクトがありません。新規作成してください。</Text></Center>
      ) : (
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>名前</Table.Th>
              <Table.Th>説明</Table.Th>
              <Table.Th>作成日時</Table.Th>
              <Table.Th>操作</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {data.data.map((p) => (
              <Table.Tr key={p.id}>
                <Table.Td>
                  <Text fw={500} component={Link} to={`/projects/${p.id}/analysis`}>{p.name}</Text>
                </Table.Td>
                <Table.Td><Text size="sm" c="dimmed" lineClamp={1}>{p.description ?? "—"}</Text></Table.Td>
                <Table.Td><Text size="sm">{new Date(p.created_at).toLocaleString("ja-JP")}</Text></Table.Td>
                <Table.Td>
                  <Group gap="xs">
                    <Button size="xs" variant="light" component={Link} to={`/projects/${p.id}/upload`}>
                      ソースアップロード
                    </Button>
                    <Button size="xs" color="red" variant="subtle" onClick={() => handleDelete(p.id, p.name)}>
                      削除
                    </Button>
                  </Group>
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      )}

      <Modal opened={opened} onClose={close} title="新規プロジェクト作成">
        <CreateProjectForm onSuccess={close} />
      </Modal>
    </>
  );
}
