from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMRequest:
    prompt: str
    context: str


@dataclass
class LLMResponse:
    content: str


class LLMClient(ABC):
    @abstractmethod
    async def complete(self, request: LLMRequest) -> LLMResponse: ...
