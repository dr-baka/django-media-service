from .minio import MinioStorageClient


def get_storage_client():
    return MinioStorageClient()
