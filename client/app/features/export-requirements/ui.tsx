import { Button } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { notifications } from "@mantine/notifications";
import { useState } from "react";
import { useExportRequirements } from "~/entities/requirement";
import { MarkdownPreviewModal } from "./ui/MarkdownPreviewModal";

interface Props {
  jobId: string;
}

export function ExportButton({ jobId }: Props) {
  const { mutateAsync, isPending } = useExportRequirements();
  const [opened, { open, close }] = useDisclosure(false);
  const [markdown, setMarkdown] = useState("");

  const handleExport = async () => {
    try {
      const md = await mutateAsync(jobId);
      setMarkdown(md);
      open();
    } catch {
      notifications.show({ title: "エラー", message: "エクスポートに失敗しました", color: "red" });
    }
  };

  return (
    <>
      <Button variant="outline" onClick={handleExport} loading={isPending}>
        Markdownエクスポート
      </Button>
      <MarkdownPreviewModal opened={opened} onClose={close} markdown={markdown} />
    </>
  );
}
