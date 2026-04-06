import axios from "axios";
import type { UploadResult } from "~/entities/source-file";

export const uploadZip = async (
  projectId: string,
  file: File,
  onUploadProgress?: (progress: number) => void,
): Promise<UploadResult> => {
  const form = new FormData();
  form.append("file", file);
  const res = await axios.post<{ data: UploadResult }>(
    `/api/v1/projects/${projectId}/upload`,
    form,
    {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress: (e) => {
        if (e.total) onUploadProgress?.(Math.round((e.loaded * 100) / e.total));
      },
    },
  );
  return res.data.data;
};
