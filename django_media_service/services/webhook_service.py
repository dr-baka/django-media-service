import hashlib, hmac, requests
from django.utils import timezone
from ..settings import get_config

def send_webhook(event: str, asset_id: str, data: dict | None = None):
    cfg = get_config()["WEBHOOK"]
    if not cfg.get("ENABLED") or not cfg.get("URL"):
        return
    payload = {"event": event, "asset_id": str(asset_id), "timestamp": timezone.now().isoformat(), "data": data or {}}
    headers = {"Content-Type": "application/json"}
    if cfg.get("SECRET"):
        sig = hmac.new(cfg["SECRET"].encode(), str(payload).encode(), hashlib.sha256).hexdigest()
        headers["X-DMS-Signature"] = sig
    try:
        requests.post(cfg["URL"], json=payload, headers=headers, timeout=5)
    except Exception:
        return
