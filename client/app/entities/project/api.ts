import { apiClient, type DataResponse, type PaginatedResponse } from "~/shared/api/client";
import type { Project, ProjectCreateInput } from "./model";

export const createProject = async (data: ProjectCreateInput): Promise<Project> => {
  const res = await apiClient.post<DataResponse<Project>>("/projects", data);
  return res.data.data;
};

export const getProjects = async (page = 1, per_page = 20): Promise<PaginatedResponse<Project>> => {
  const res = await apiClient.get<PaginatedResponse<Project>>("/projects", {
    params: { page, per_page },
  });
  return res.data;
};

export const getProject = async (id: string): Promise<Project> => {
  const res = await apiClient.get<DataResponse<Project>>(`/projects/${id}`);
  return res.data.data;
};

export const deleteProject = async (id: string): Promise<void> => {
  await apiClient.delete(`/projects/${id}`);
};
