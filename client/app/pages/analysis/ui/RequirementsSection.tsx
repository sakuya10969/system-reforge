import { Badge, Button, Card, Group, Modal, Select, Skeleton, Stack, Text, Textarea, TextInput, Title } from "@mantine/core";
import { useForm } from "@mantine/form";
import { useDisclosure } from "@mantine/hooks";
import { notifications } from "@mantine/notifications";
import { useState } from "react";
import type { Requirement, RequirementPriority, RequirementStatus } from "~/entities/requirement";
import { useUpdateRequirement } from "~/entities/requirement";

const PRIORITY_COLOR: Record<RequirementPriority, string> = { low: "gray", medium: "yellow", high: "red" };
const STATUS_COLOR: Record<RequirementStatus, string> = { draft: "gray", reviewed: "blue", approved: "green" };
const PRIORITY_LABEL: Record<RequirementPriority, string> = { low: "低", medium: "中", high: "高" };
const STATUS_LABEL: Record<RequirementStatus, string> = { draft: "ドラフト", reviewed: "レビュー済", approved: "承認済" };

interface EditModalProps {
  req: Requirement;
  jobId: string;
  opened: boolean;
  onClose: () => void;
}

function EditModal({ req, jobId, opened, onClose }: EditModalProps) {
  const { mutateAsync, isPending } = useUpdateRequirement(jobId);
  const form = useForm({
    initialValues: {
      title: req.title,
      description: req.description,
      priority: req.priority,
      status: req.status,
    },
    validate: {
      title: (v) => (!v.trim() ? "タイトルは必須です" : null),
      description: (v) => (!v.trim() ? "説明は必須です" : null),
    },
  });

  const handleSubmit = form.onSubmit(async (values) => {
    try {
      await mutateAsync({ id: req.id, data: values });
      notifications.show({ title: "更新完了", message: "要件を更新しました", color: "green" });
      onClose();
    } catch {
      notifications.show({ title: "エラー", message: "更新に失敗しました", color: "red" });
    }
  });

  return (
    <Modal opened={opened} onClose={onClose} title="要件編集">
      <form onSubmit={handleSubmit}>
        <Stack>
          <TextInput label="タイトル" required {...form.getInputProps("title")} />
          <Textarea label="説明" required rows={4} {...form.getInputProps("description")} />
          <Select label="優先度" data={[{ value: "low", label: "低" }, { value: "medium", label: "中" }, { value: "high", label: "高" }]} {...form.getInputProps("priority")} />
          <Select label="ステータス" data={[{ value: "draft", label: "ドラフト" }, { value: "reviewed", label: "レビュー済" }, { value: "approved", label: "承認済" }]} {...form.getInputProps("status")} />
          <Group justify="flex-end">
            <Button variant="outline" onClick={onClose}>キャンセル</Button>
            <Button type="submit" loading={isPending}>保存</Button>
          </Group>
        </Stack>
      </form>
    </Modal>
  );
}

interface Props {
  requirements: Requirement[] | undefined;
  isLoading: boolean;
  jobId: string;
}

export function RequirementsSection({ requirements, isLoading, jobId }: Props) {
  const [editTarget, setEditTarget] = useState<Requirement | null>(null);
  const [opened, { open, close }] = useDisclosure(false);

  if (isLoading) return <Skeleton height={300} />;
  if (!requirements || requirements.length === 0) {
    return <Text c="dimmed" ta="center" py="xl">要件がありません</Text>;
  }

  return (
    <>
      <Stack>
        {requirements.map((req) => (
          <Card key={req.id} withBorder shadow="xs" padding="md">
            <Group justify="space-between" mb="xs">
              <Title order={5}>{req.title}</Title>
              <Group gap="xs">
                <Badge color={PRIORITY_COLOR[req.priority]}>{PRIORITY_LABEL[req.priority]}</Badge>
                <Badge color={STATUS_COLOR[req.status]}>{STATUS_LABEL[req.status]}</Badge>
              </Group>
            </Group>
            <Text size="sm" mb="xs">{req.description}</Text>
            {req.category && <Text size="xs" c="dimmed">カテゴリ: {req.category}</Text>}
            <Group justify="flex-end" mt="sm">
              <Button size="xs" variant="light" onClick={() => { setEditTarget(req); open(); }}>
                編集
              </Button>
            </Group>
          </Card>
        ))}
      </Stack>

      {editTarget && (
        <EditModal req={editTarget} jobId={jobId} opened={opened} onClose={() => { close(); setEditTarget(null); }} />
      )}
    </>
  );
}
