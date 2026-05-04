import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from .base import BaseStorageClient
from ..settings import get_config


class MinioStorageClient(BaseStorageClient):
    def __init__(self):
        cfg = get_config()["STORAGE"]
        self.bucket = cfg["BUCKET_NAME"]
        self.client = boto3.client("s3", endpoint_url=("https" if cfg["USE_SSL"] else "http") + "://" + cfg["ENDPOINT"], aws_access_key_id=cfg["ACCESS_KEY"], aws_secret_access_key=cfg["SECRET_KEY"], config=Config(signature_version="s3v4"))

    def generate_presigned_put_url(self, key, expires, content_type=None):
        params = {"Bucket": self.bucket, "Key": key}
        if content_type:
            params["ContentType"] = content_type
        return self.client.generate_presigned_url("put_object", Params=params, ExpiresIn=expires)

    def generate_presigned_get_url(self, key, expires):
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
            self.client.delete_object(Bucket=self.bucket, Key=key)
