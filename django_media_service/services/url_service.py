from ..settings import get_config
from ..storage import get_storage_client

def sign_get_url(key: str):
    cfg = get_config()["STORAGE"]
    return get_storage_client().generate_presigned_get_url(key, cfg["SIGNED_URL_EXPIRE_SECONDS"])
