import { apiClient, type DataResponse } from "~/shared/api/client";
import type { Requirement, RequirementUpdateInput } from "./model";

export const listByJob = async (jobId: string): Promise<Requirement[]> => {
  const res = await apiClient.get<{ data: Requirement[] }>(`/jobs/${jobId}/requirements`);
  return res.data.data;
};

export const update = async (id: string, data: RequirementUpdateInput): Promise<Requirement> => {
  const res = await apiClient.put<DataResponse<Requirement>>(`/requirements/${id}`, data);
  return res.data.data;
};

export const exportRequirements = async (jobId: string): Promise<string> => {
  const res = await apiClient.post<{ data: { markdown: string } }>(`/jobs/${jobId}/requirements/export`);
  return res.data.data.markdown;
};
