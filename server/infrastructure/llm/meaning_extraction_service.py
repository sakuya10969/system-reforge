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
                        prompt=f"Extract business rules from the following code in {data.language or 'unknown'} language.",
                        context=data.content,
                    )
                )
                rules = json.loads(response.content)
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
