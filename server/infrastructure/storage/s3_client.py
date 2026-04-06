import boto3

from server.config.settings import Settings, get_settings
from server.domain.services.storage_client import StorageClient


class S3Client(StorageClient):
    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._bucket_name = self._settings.s3_bucket_name
        self._client = boto3.client(
            "s3",
            region_name=self._settings.s3_region,
            aws_access_key_id=self._settings.aws_access_key_id,
            aws_secret_access_key=self._settings.aws_secret_access_key,
        )

    def generate_source_key(self, s3_prefix: str, file_path: str) -> str:
        return f"{s3_prefix}/sources/{file_path}"

    def upload_file(self, key: str, content: bytes) -> None:
        self._client.put_object(Bucket=self._bucket_name, Key=key, Body=content)
