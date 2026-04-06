import os

import boto3


class S3Client:
    def __init__(self, bucket_name: str | None = None) -> None:
        self._bucket_name = bucket_name or os.environ.get("S3_BUCKET_NAME", "system-reforge")
        region = os.environ.get("AWS_DEFAULT_REGION") or os.environ.get("AWS_BEDROCK_REGION")
        self._client = boto3.client("s3", region_name=region)

    def generate_s3_key(self, s3_prefix: str, file_path: str) -> str:
        return f"{s3_prefix}/sources/{file_path}"

    def upload_file(self, key: str, content: bytes) -> None:
        self._client.put_object(Bucket=self._bucket_name, Key=key, Body=content)
