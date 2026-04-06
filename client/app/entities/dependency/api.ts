import { apiClient } from "~/shared/api/client";
import type { DependencyGraph, FlowData } from "./model";
import type { SourceFile } from "~/entities/source-file";

export const getDependencies = async (jobId: string): Promise<DependencyGraph> => {
  const res = await apiClient.get<{ data: DependencyGraph }>(`/jobs/${jobId}/dependencies`);
  return res.data.data;
};

export const getFlow = async (jobId: string): Promise<FlowData> => {
  const res = await apiClient.get<{ data: FlowData }>(`/jobs/${jobId}/flow`);
  return res.data.data;
};

export const getSourceFiles = async (jobId: string): Promise<SourceFile[]> => {
  const res = await apiClient.get<{ data: SourceFile[] }>(`/jobs/${jobId}/source-files`);
  return res.data.data;
};
