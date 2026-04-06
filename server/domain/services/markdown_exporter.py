from server.domain.models.requirement import Requirement


class MarkdownExporter:
    def to_markdown(self, requirements: list[Requirement]) -> str:
        lines = ["# 要件定義書"]
        for req in requirements:
            lines.append(f"\n## {req.title}")
            lines.append(f"- **説明**: {req.description}")
            if req.category:
                lines.append(f"- **カテゴリ**: {req.category}")
            lines.append(f"- **優先度**: {req.priority.value}")
            lines.append(f"- **ステータス**: {req.status.value}")
        return "\n".join(lines)
