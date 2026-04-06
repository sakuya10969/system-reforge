import { apiClient, type DataResponse } from "~/shared/api/client";
import type { Job } from "./model";

export const createJob = async (projectId: string): Promise<Job> => {
  const res = await apiClient.post<DataResponse<Job>>(`/projects/${projectId}/jobs`);
  return res.data.data;
};

export const listJobs = async (projectId: string): Promise<Job[]> => {
  const res = await apiClient.get<{ data: Job[] }>(`/projects/${projectId}/jobs`);
  return res.data.data;
};

export const getJob = async (jobId: string): Promise<Job> => {
  const res = await apiClient.get<DataResponse<Job>>(`/jobs/${jobId}`);
  return res.data.data;
};
