from .minio import MinioStorageClient, RustFSStorageClient, S3ObjectStorageClient
from ..settings import get_config


def get_storage_client():
    backend = get_config()["STORAGE"]["BACKEND"].lower()
    if backend == "rustfs":
        return RustFSStorageClient()
    if backend == "minio":
        return MinioStorageClient()
    if backend in {"s3", "aws", "aws_s3"}:
        return S3ObjectStorageClient(endpoint=None)
    raise ValueError(f"Unsupported storage backend: {backend}")
