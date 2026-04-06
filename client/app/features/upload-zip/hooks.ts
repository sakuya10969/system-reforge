import { useState } from "react";
import { uploadZip } from "./api";
import type { UploadResult } from "~/entities/source-file";

export function useUploadZip() {
  const [isPending, setIsPending] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<UploadResult | null>(null);

  const mutate = async (projectId: string, file: File) => {
    setIsPending(true);
    setError(null);
    setProgress(0);
    try {
      const res = await uploadZip(projectId, file, setProgress);
      setResult(res);
      return res;
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "アップロードに失敗しました";
      setError(msg);
      throw e;
    } finally {
      setIsPending(false);
    }
  };

  return { mutate, isPending, progress, error, result };
}
