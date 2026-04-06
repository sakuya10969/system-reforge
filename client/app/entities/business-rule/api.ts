import { apiClient } from "~/shared/api/client";
import type { BusinessRule, RuleType } from "./model";

export const listByJob = async (jobId: string, ruleType?: RuleType): Promise<BusinessRule[]> => {
  const res = await apiClient.get<{ data: BusinessRule[] }>(`/jobs/${jobId}/business-rules`, {
    params: ruleType ? { rule_type: ruleType } : undefined,
  });
  return res.data.data;
};
