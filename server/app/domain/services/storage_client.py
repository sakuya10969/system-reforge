from abc import ABC, abstractmethod


class StorageClient(ABC):
    @abstractmethod
    def generate_source_key(self, s3_prefix: str, file_path: str) -> str: ...

    @abstractmethod
    def upload_file(self, key: str, content: bytes) -> None: ...
