import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createJob, getJob, listJobs } from "./api";
import type { JobStatus } from "./model";

const isPolling = (status: JobStatus) => status === "pending" || status === "running";

export const useJobs = (projectId: string) =>
  useQuery({
    queryKey: ["jobs", projectId],
    queryFn: () => listJobs(projectId),
    enabled: !!projectId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (!data) return false;
      return data.some((j) => isPolling(j.status)) ? 5000 : false;
    },
  });

export const useJob = (jobId: string) =>
  useQuery({
    queryKey: ["jobs", "detail", jobId],
    queryFn: () => getJob(jobId),
    enabled: !!jobId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (!data) return false;
      return isPolling(data.status) ? 5000 : false;
    },
  });

export const useCreateJob = (projectId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => createJob(projectId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["jobs", projectId] }),
  });
};
