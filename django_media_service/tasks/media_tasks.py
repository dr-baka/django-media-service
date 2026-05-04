from celery import shared_task
from ..models import MediaAsset
from ..settings import get_config
from ..services.thumbnail_service import generate_for_asset as generate_thumb
from ..services.hls_service import generate_for_asset as generate_hls_data
from ..services.webhook_service import send_webhook
from ..storage import get_storage_client


@shared_task
def process_metadata(asset_id):
    return str(asset_id)


@shared_task
def generate_thumbnails(asset_id):
    asset = MediaAsset.objects.get(id=asset_id)
    asset.thumbnail_status = "processing"
    asset.save(update_fields=["thumbnail_status"])
    try:
        asset.thumbnail_data = generate_thumb(asset)
        asset.thumbnail_status = "ready"
        asset.save(update_fields=["thumbnail_data", "thumbnail_status"])
        send_webhook("thumbnail.ready", str(asset.id), asset.thumbnail_data)
    except Exception as exc:
        asset.thumbnail_status = "failed"
        asset.processing_error = str(exc)
        asset.save(update_fields=["thumbnail_status", "processing_error"])
        send_webhook("thumbnail.failed", str(asset.id), {"error": str(exc)})


@shared_task
def generate_hls(asset_id):
    asset = MediaAsset.objects.get(id=asset_id)
    cfg = get_config()["HLS"]
    asset.hls_status = "processing"
    asset.save(update_fields=["hls_status"])
    try:
        asset.hls_data = generate_hls_data(asset, cfg["BITRATES"])
        asset.hls_status = "ready"
        asset.save(update_fields=["hls_data", "hls_status"])
        send_webhook("hls.ready", str(asset.id), asset.hls_data)
    except Exception as exc:
        asset.hls_status = "failed"
        asset.processing_error = str(exc)
        asset.save(update_fields=["hls_status", "processing_error"])
        send_webhook("hls.failed", str(asset.id), {"error": str(exc)})


@shared_task
def cleanup_media_files(asset_id):
    prefix = f"media/{asset_id}/"
    get_storage_client().delete_prefix(prefix)


@shared_task
def dispatch_webhook(event, asset_id):
    send_webhook(event, asset_id)
