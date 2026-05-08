import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from .base import BaseStorageClient
from ..settings import get_config


class S3ObjectStorageClient(BaseStorageClient):
    def __init__(self, endpoint: str | None = None):
        cfg = get_config()["STORAGE"]
        self.bucket = cfg["BUCKET_NAME"]
        endpoint_url = None
        if endpoint:
            endpoint_url = ("https" if cfg["USE_SSL"] else "http") + "://" + endpoint
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=cfg["ACCESS_KEY"],
            aws_secret_access_key=cfg["SECRET_KEY"],
            config=Config(signature_version="s3v4"),
            region_name=cfg.get("REGION_NAME"),
        )

    def put_object(self, key, body, content_type=None):
        params = {"Bucket": self.bucket, "Key": key, "Body": body}
        if content_type:
            params["ContentType"] = content_type
        self.client.put_object(**params)

    def get_object(self, key):
        return self.client.get_object(Bucket=self.bucket, Key=key)

    def delete_object(self, key):
        self.client.delete_object(Bucket=self.bucket, Key=key)

    def generate_presigned_put_url(self, key, expires, content_type=None):
        return self.presign_put(key, expires, content_type)

    def presign_put(self, key, expires, content_type=None):
        params = {"Bucket": self.bucket, "Key": key}
        if content_type:
            params["ContentType"] = content_type
        return self.client.generate_presigned_url("put_object", Params=params, ExpiresIn=expires)

    def generate_presigned_get_url(self, key, expires):
        return self.presign_get(key, expires)

    def presign_get(self, key, expires):
        return self.client.generate_presigned_url("get_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=expires)

    def object_exists(self, key):
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError:
            return False

    def list_keys(self, prefix):
        res = self.client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        return [o["Key"] for o in res.get("Contents", [])]

    def delete_prefix(self, prefix):
        for key in self.list_keys(prefix):
            self.delete_object(key)


class RustFSStorageClient(S3ObjectStorageClient):
    def __init__(self):
        super().__init__(endpoint=get_config()["STORAGE"]["ENDPOINT"])


class MinioStorageClient(S3ObjectStorageClient):
    def __init__(self):
        super().__init__(endpoint=get_config()["STORAGE"]["ENDPOINT"])
