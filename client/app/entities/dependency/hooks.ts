import { useQuery } from "@tanstack/react-query";
import { getDependencies, getFlow, getSourceFiles } from "./api";

export const useDependencyGraph = (jobId: string) =>
  useQuery({
    queryKey: ["dependencies", jobId],
    queryFn: () => getDependencies(jobId),
    enabled: !!jobId,
  });

export const useFlowData = (jobId: string) =>
  useQuery({
    queryKey: ["flow", jobId],
    queryFn: () => getFlow(jobId),
    enabled: !!jobId,
  });

export const useSourceFiles = (jobId: string) =>
  useQuery({
    queryKey: ["source-files", jobId],
    queryFn: () => getSourceFiles(jobId),
    enabled: !!jobId,
  });
