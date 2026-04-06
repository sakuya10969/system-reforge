import { Button, Group, Modal, ScrollArea } from "@mantine/core";
import ReactMarkdown from "react-markdown";

interface Props {
  opened: boolean;
  onClose: () => void;
  markdown: string;
}

export function MarkdownPreviewModal({ opened, onClose, markdown }: Props) {
  const handleDownload = () => {
    const blob = new Blob([markdown], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "requirements.md";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Modal opened={opened} onClose={onClose} title="要件定義書プレビュー" size="xl">
      <ScrollArea h={500}>
        <ReactMarkdown>{markdown}</ReactMarkdown>
      </ScrollArea>
      <Group justify="flex-end" mt="md">
        <Button variant="outline" onClick={onClose}>閉じる</Button>
        <Button onClick={handleDownload}>ダウンロード</Button>
      </Group>
    </Modal>
  );
}
