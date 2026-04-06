export interface Project {
  id: string;
  name: string;
  description: string | null;
  s3_prefix: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreateInput {
  name: string;
  description?: string;
}
