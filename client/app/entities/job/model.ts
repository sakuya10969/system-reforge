export type JobStatus = "pending" | "running" | "completed" | "failed";

export interface Job {
  id: string;
  project_id: string;
  status: JobStatus;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
}
