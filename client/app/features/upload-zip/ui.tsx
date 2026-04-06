import { Alert, Badge, Button, Group, Progress, Stack, Text } from "@mantine/core";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { useUploadZip } from "./hooks";

interface Props {
  projectId: string;
  onSuccess?: () => void;
}

export function UploadDropzone({ projectId, onSuccess }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const { mutate, isPending, progress, error, result } = useUploadZip();

  const onDrop = useCallback((accepted: File[]) => {
    if (accepted[0]) setFile(accepted[0]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/zip": [".zip"], "application/x-zip-compressed": [".zip"] },
    multiple: false,
    disabled: isPending,
  });

  const handleUpload = async () => {
    if (!file) return;
    await mutate(projectId, file);
    onSuccess?.();
  };

  return (
    <Stack>
      <div
        {...getRootProps()}
        style={{
          border: "2px dashed #ced4da",
          borderRadius: 8,
          padding: "2rem",
          textAlign: "center",
          cursor: isPending ? "not-allowed" : "pointer",
          background: isDragActive ? "#f8f9fa" : "white",
        }}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <Text c="blue">ここにドロップ</Text>
        ) : (
          <Text c="dimmed">ZIPファイルをドラッグ＆ドロップ、またはクリックして選択</Text>
        )}
      </div>

      {file && (
        <Group>
          <Text size="sm">{file.name}</Text>
          <Badge variant="light">{(file.size / 1024).toFixed(1)} KB</Badge>
        </Group>
      )}

      {isPending && <Progress value={progress} animated />}

      {error && <Alert color="red" title="エラー">{error}</Alert>}

      {result && (
        <Alert color="green" title="アップロード完了">
          {result.total_files} ファイルをアップロードしました
        </Alert>
      )}

      <Button onClick={handleUpload} disabled={!file || isPending} loading={isPending}>
        アップロード
      </Button>
    </Stack>
  );
}
