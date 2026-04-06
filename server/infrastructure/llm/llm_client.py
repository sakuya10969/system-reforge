from server.domain.services.llm_client import LLMClient, LLMRequest, LLMResponse


class StubLLMClient(LLMClient):
    async def complete(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            content='[{"rule_type":"condition","description":"If order amount exceeds limit, require approval"},{"rule_type":"calculation","description":"Total price = unit price * quantity * (1 - discount)"},{"rule_type":"validation","description":"Customer age must be 18 or older"}]'
        )
