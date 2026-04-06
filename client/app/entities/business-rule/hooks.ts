import { useQuery } from "@tanstack/react-query";
import { listByJob } from "./api";
import type { RuleType } from "./model";

export const useBusinessRules = (jobId: string, ruleType?: RuleType) =>
  useQuery({
    queryKey: ["business-rules", jobId, ruleType],
    queryFn: () => listByJob(jobId, ruleType),
    enabled: !!jobId,
  });
