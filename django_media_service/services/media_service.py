import os
from ..models import MediaAsset
from .metadata_service import detect_media_type
from ..storage import get_storage_client

def build_original_key(asset_id, filename):
    return f"media/{asset_id}/original/{filename}"

def create_asset(owner, filename, file_key, mime_type, file_size, thumbnail_enabled=False, hls_enabled=False, is_private=True):
    asset = MediaAsset.objects.create(owner=owner, original_filename=filename, file_key=file_key, bucket_name=get_storage_client().bucket, mime_type=mime_type, extension=os.path.splitext(filename)[1].replace('.', ''), file_size=file_size, media_type=detect_media_type(mime_type), thumbnail_enabled=thumbnail_enabled, hls_enabled=hls_enabled, thumbnail_status="pending" if thumbnail_enabled else "disabled", hls_status="pending" if hls_enabled else "disabled", is_private=is_private)
    return asset
