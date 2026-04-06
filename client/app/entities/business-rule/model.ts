export type RuleType = "condition" | "calculation" | "validation";

export interface SourceLocation {
  file_path: string;
  start_line: number | null;
  end_line: number | null;
}

export interface BusinessRule {
  id: string;
  job_id: string;
  source_file_id: string | null;
  rule_type: RuleType;
  description: string;
  source_location: SourceLocation | null;
  created_at: string;
}
