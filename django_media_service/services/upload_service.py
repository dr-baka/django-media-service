import uuid
from ..exceptions import ValidationError
from ..settings import get_config
from ..storage import get_storage_client

def validate_upload(mime_type: str, file_size: int):
    cfg = get_config()["UPLOAD"]
    if file_size > cfg["MAX_FILE_SIZE_MB"] * 1024 * 1024:
        raise ValidationError("File too large")
    allowed = cfg["ALLOWED_MIME_TYPES"]
    if "*" not in allowed and mime_type not in allowed:
        raise ValidationError("MIME type not allowed")

def create_presign(filename, mime_type):
    cfg = get_config()
    temp_key = f"media/tmp/{uuid.uuid4()}-{filename}"
    url = get_storage_client().generate_presigned_put_url(temp_key, cfg["UPLOAD"]["PRESIGNED_EXPIRE_SECONDS"], mime_type)
    return temp_key, url
