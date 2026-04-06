import { Button } from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { useCreateJob } from "~/entities/job";

interface Props {
  projectId: string;
}

export function StartAnalysisButton({ projectId }: Props) {
  const { mutateAsync, isPending } = useCreateJob(projectId);

  const handleClick = async () => {
    try {
      await mutateAsync();
      notifications.show({ title: "解析開始", message: "解析ジョブを開始しました", color: "blue" });
    } catch {
      notifications.show({ title: "エラー", message: "解析の開始に失敗しました", color: "red" });
    }
  };

  return (
    <Button onClick={handleClick} loading={isPending} color="blue">
      解析開始
    </Button>
  );
}
