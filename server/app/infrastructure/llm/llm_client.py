import json
import logging

import boto3

from app.config.settings import Settings, get_settings
from app.domain.services.llm_client import LLMClient, LLMRequest, LLMResponse

logger = logging.getLogger(__name__)


class StubLLMClient(LLMClient):
    async def complete(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            content='[{"rule_type":"condition","description":"If order amount exceeds limit, require approval"},{"rule_type":"calculation","description":"Total price = unit price * quantity * (1 - discount)"},{"rule_type":"validation","description":"Customer age must be 18 or older"}]'
        )


class BedrockLLMClient(LLMClient):
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        if not self._settings.aws_bedrock_model_id:
            raise ValueError("AWS_BEDROCK_MODEL_ID is required to use BedrockLLMClient")

        self._client = boto3.client(
            "bedrock-runtime",
            region_name=self._settings.bedrock_region,
            aws_access_key_id=self._settings.aws_access_key_id,
            aws_secret_access_key=self._settings.aws_secret_access_key,
        )

    async def complete(self, request: LLMRequest) -> LLMResponse:
        user_text = f"{request.prompt}\n\nContext:\n{request.context}"
        response = self._client.converse(
            modelId=self._settings.aws_bedrock_model_id,
            system=[{"text": request.system_prompt}],
            messages=[
                {
                    "role": "user",
                    "content": [{"text": user_text}],
                }
            ],
            inferenceConfig={
                "temperature": request.temperature,
                "maxTokens": request.max_tokens,
            },
        )

        content = self._extract_text(response)
        logger.debug("Received response from Bedrock model %s", self._settings.aws_bedrock_model_id)
        return LLMResponse(content=content)

    @staticmethod
    def _extract_text(response: dict) -> str:
        parts = response.get("output", {}).get("message", {}).get("content", [])
        texts = [part.get("text", "") for part in parts if "text" in part]
        if not texts:
            raise ValueError(f"Bedrock response did not contain text content: {json.dumps(response)}")
        return "\n".join(texts)
