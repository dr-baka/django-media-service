from abc import ABC, abstractmethod


class BaseStorageClient(ABC):
    @abstractmethod
    def put_object(self, key: str, body: bytes, content_type: str | None = None): ...

    @abstractmethod
    def get_object(self, key: str): ...

    @abstractmethod
    def delete_object(self, key: str): ...

    @abstractmethod
    def presign_get(self, key: str, expires: int): ...

    @abstractmethod
    def presign_put(self, key: str, expires: int, content_type: str | None = None): ...

    @abstractmethod
    def generate_presigned_put_url(self, key: str, expires: int, content_type: str | None = None): ...

    @abstractmethod
    def generate_presigned_get_url(self, key: str, expires: int): ...

    @abstractmethod
    def object_exists(self, key: str) -> bool: ...

    @abstractmethod
    def delete_prefix(self, prefix: str): ...
