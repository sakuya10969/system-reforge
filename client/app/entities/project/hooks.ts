import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createProject, deleteProject, getProject, getProjects } from "./api";
import type { ProjectCreateInput } from "./model";

export const useProjects = (page = 1, perPage = 20) =>
  useQuery({
    queryKey: ["projects", page, perPage],
    queryFn: () => getProjects(page, perPage),
  });

export const useProject = (id: string) =>
  useQuery({
    queryKey: ["projects", id],
    queryFn: () => getProject(id),
    enabled: !!id,
  });

export const useCreateProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ProjectCreateInput) => createProject(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["projects"] }),
  });
};

export const useDeleteProject = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteProject(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["projects"] }),
  });
};
