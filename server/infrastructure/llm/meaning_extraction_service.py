import json
import logging

from server.domain.services.llm_client import LLMClient, LLMRequest
from server.domain.services.meaning_extraction_service import (
    ExtractedRule,
    IntermediateData,
    MeaningExtractionService,
)

logger = logging.getLogger(__name__)


class DefaultMeaningExtractionService(MeaningExtractionService):
    def __init__(self, llm_client: LLMClient) -> None:
        self._llm_client = llm_client

    async def extract(self, data_list: list[IntermediateData]) -> list[ExtractedRule]:
        results: list[ExtractedRule] = []
        for data in data_list:
            try:
                response = await self._llm_client.complete(
                    LLMRequest(
                        system_prompt=(
                            "You extract business rules from structured intermediate data only. "
                            "Return JSON only as an array of objects with keys: "
                            "rule_type, description, source_file_path, start_line, end_line."
                        ),
                        prompt=(
                            f"Extract business rules for the file {data.file_path} "
                            f"written in {data.language or 'unknown'}."
                        ),
                        context=json.dumps(
                            {
                                "file_path": data.file_path,
                                "language": data.language,
                                "intermediate_data": data.content,
                            },
                            ensure_ascii=True,
                        ),
                    )
                )
                rules = json.loads(_strip_json_fence(response.content))
                for rule in rules:
                    results.append(
                        ExtractedRule(
                            rule_type=rule.get("rule_type", "condition"),
                            description=rule.get("description", ""),
                            source_file_path=data.file_path,
                        )
                    )
            except Exception as e:
                logger.warning("Failed to extract rules from %s: %s", data.file_path, e)
        return results


def _strip_json_fence(content: str) -> str:
    stripped = content.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3:
            return "\n".join(lines[1:-1]).strip()
    return stripped
