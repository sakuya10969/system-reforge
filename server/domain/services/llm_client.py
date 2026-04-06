from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMRequest:
    system_prompt: str
    prompt: str
    context: str
    temperature: float = 0.0
    max_tokens: int = 1000


@dataclass
class LLMResponse:
    content: str


class LLMClient(ABC):
    @abstractmethod
    async def complete(self, request: LLMRequest) -> LLMResponse: ...
