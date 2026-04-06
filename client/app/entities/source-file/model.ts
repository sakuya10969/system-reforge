export interface SourceFile {
  id: string;
  project_id: string;
  file_path: string;
  language: string | null;
  s3_key: string;
}

export interface UploadedFile {
  file_path: string;
  language: string | null;
  s3_key: string;
}

export interface UploadResult {
  project_id: string;
  total_files: number;
  uploaded_files: UploadedFile[];
}
