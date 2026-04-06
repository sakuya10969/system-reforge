import { Button, Stack, Textarea, TextInput } from "@mantine/core";
import { useForm } from "@mantine/form";
import { notifications } from "@mantine/notifications";
import { useCreateProject } from "~/entities/project";

interface Props {
  onSuccess?: () => void;
}

export function CreateProjectForm({ onSuccess }: Props) {
  const form = useForm({
    initialValues: { name: "", description: "" },
    validate: {
      name: (v) => (!v.trim() ? "プロジェクト名は必須です" : v.length > 255 ? "255文字以内で入力してください" : null),
    },
  });

  const { mutateAsync, isPending } = useCreateProject();

  const handleSubmit = form.onSubmit(async (values) => {
    try {
      await mutateAsync({ name: values.name.trim(), description: values.description || undefined });
      notifications.show({ title: "作成完了", message: "プロジェクトを作成しました", color: "green" });
      form.reset();
      onSuccess?.();
    } catch {
      notifications.show({ title: "エラー", message: "プロジェクトの作成に失敗しました", color: "red" });
    }
  });

  return (
    <form onSubmit={handleSubmit}>
      <Stack>
        <TextInput label="プロジェクト名" placeholder="例: レガシー基幹システム" required {...form.getInputProps("name")} />
        <Textarea label="説明" placeholder="プロジェクトの概要（任意）" rows={3} {...form.getInputProps("description")} />
        <Button type="submit" loading={isPending}>作成</Button>
      </Stack>
    </form>
  );
}
