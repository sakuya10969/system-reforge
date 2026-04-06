import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { exportRequirements, listByJob, update } from "./api";
import type { RequirementUpdateInput } from "./model";

export const useRequirements = (jobId: string) =>
  useQuery({
    queryKey: ["requirements", jobId],
    queryFn: () => listByJob(jobId),
    enabled: !!jobId,
  });

export const useUpdateRequirement = (jobId: string) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: RequirementUpdateInput }) => update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["requirements", jobId] }),
  });
};

export const useExportRequirements = () =>
  useMutation({
    mutationFn: (jobId: string) => exportRequirements(jobId),
  });
