import { Center, Select, Skeleton, Stack, Table, Text } from "@mantine/core";
import { useState } from "react";
import type { BusinessRule, RuleType } from "~/entities/business-rule";
import { RuleTypeBadge } from "./RuleTypeBadge";

interface Props {
  rules: BusinessRule[] | undefined;
  isLoading: boolean;
}

export function RuleTable({ rules, isLoading }: Props) {
  const [filterType, setFilterType] = useState<RuleType | "">("");

  if (isLoading) return <Skeleton height={200} />;

  const filtered = filterType ? rules?.filter((r) => r.rule_type === filterType) : rules;

  return (
    <Stack>
      <Select
        placeholder="種別フィルタ"
        clearable
        data={[
          { value: "condition", label: "条件" },
          { value: "calculation", label: "計算" },
          { value: "validation", label: "検証" },
        ]}
        value={filterType}
        onChange={(v) => setFilterType((v ?? "") as RuleType | "")}
        w={200}
      />

      {!filtered || filtered.length === 0 ? (
        <Center py="xl"><Text c="dimmed">業務ルールがありません</Text></Center>
      ) : (
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>種別</Table.Th>
              <Table.Th>説明</Table.Th>
              <Table.Th>ソースファイル</Table.Th>
              <Table.Th>位置</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {filtered.map((rule) => (
              <Table.Tr key={rule.id}>
                <Table.Td><RuleTypeBadge type={rule.rule_type} /></Table.Td>
                <Table.Td><Text size="sm">{rule.description}</Text></Table.Td>
                <Table.Td>
                  <Text size="xs" ff="monospace" c="dimmed">
                    {rule.source_location?.file_path ?? "—"}
                  </Text>
                </Table.Td>
                <Table.Td>
                  <Text size="xs">
                    {rule.source_location?.start_line != null
                      ? `L${rule.source_location.start_line}–${rule.source_location.end_line ?? rule.source_location.start_line}`
                      : "—"}
                  </Text>
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      )}
    </Stack>
  );
}
