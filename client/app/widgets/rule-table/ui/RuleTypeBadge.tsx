import { Badge } from "@mantine/core";
import type { RuleType } from "~/entities/business-rule";

const COLOR: Record<RuleType, string> = {
  condition: "blue",
  calculation: "green",
  validation: "orange",
};

const LABEL: Record<RuleType, string> = {
  condition: "条件",
  calculation: "計算",
  validation: "検証",
};

export function RuleTypeBadge({ type }: { type: RuleType }) {
  return <Badge color={COLOR[type]}>{LABEL[type]}</Badge>;
}
