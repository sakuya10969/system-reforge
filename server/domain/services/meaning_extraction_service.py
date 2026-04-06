from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class IntermediateData:
    file_path: str
    content: str
    language: str | None = None


@dataclass
class ExtractedRule:
    rule_type: str
    description: str
    source_file_path: str | None = None
    start_line: int | None = None
    end_line: int | None = None


class MeaningExtractionService(ABC):
    @abstractmethod
    async def extract(self, data_list: list[IntermediateData]) -> list[ExtractedRule]: ...
