export type RequirementStatus = "draft" | "reviewed" | "approved";
export type RequirementPriority = "low" | "medium" | "high";

export interface Requirement {
  id: string;
  job_id: string;
  title: string;
  description: string;
  category: string | null;
  priority: RequirementPriority;
  status: RequirementStatus;
  source_rules: string[];
  created_at: string;
  updated_at: string;
}

export interface RequirementUpdateInput {
  title?: string;
  description?: string;
  category?: string;
  priority?: RequirementPriority;
  status?: RequirementStatus;
}
