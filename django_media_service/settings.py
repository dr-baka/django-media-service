from copy import deepcopy
from django.conf import settings as django_settings


DEFAULTS = {
    "UPLOAD": {
        "DEFAULT_MODE": "presigned",
        "ENABLE_DJANGO_UPLOAD": True,
        "MAX_FILE_SIZE_MB": 100,
        "PRESIGNED_EXPIRE_SECONDS": 3600,
        "ALLOWED_MIME_TYPES": ["*"],
    },
    "STORAGE": {
        "BACKEND": "minio",
        "ENDPOINT": "localhost:9000",
        "ACCESS_KEY": "minioadmin",
        "SECRET_KEY": "minioadmin",
        "BUCKET_NAME": "media",
        "USE_SSL": False,
        "DEFAULT_PRIVATE": True,
        "SIGNED_URL_EXPIRE_SECONDS": 3600,
    },
    "PERMISSIONS": {
        "DEFAULT_PERMISSION_CLASS": "django_media_service.api.permissions.IsOwnerOrAdmin",
    },
    "THUMBNAIL": {
        "ENABLED": False,
        "AUTO_GENERATE": False,
        "VIDEO_FRAME_PERCENT": 10,
        "SIZES": {"small": [320, 180], "medium": [640, 360], "large": [1280, 720]},
    },
    "HLS": {
        "ENABLED": False,
        "AUTO_GENERATE": False,
        "SIGNED_PLAYBACK": True,
        "BITRATES": {
            "360p": {"width": 640, "height": 360, "video_bitrate": "800k", "audio_bitrate": "96k"},
            "720p": {"width": 1280, "height": 720, "video_bitrate": "2800k", "audio_bitrate": "128k"},
            "1080p": {"width": 1920, "height": 1080, "video_bitrate": "5000k", "audio_bitrate": "192k"},
        },
    },
    "WEBHOOK": {
        "ENABLED": False,
        "URL": None,
        "SECRET": None,
        "EVENTS": ["media.uploaded", "thumbnail.ready", "thumbnail.failed", "hls.ready", "hls.failed", "media.deleted"],
    },
}


def _deep_update(target, src):
    for key, value in src.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_update(target[key], value)
        else:
            target[key] = value


def get_config():
    cfg = deepcopy(DEFAULTS)
    user_cfg = getattr(django_settings, "DJANGO_MEDIA_SERVICE", {})
    _deep_update(cfg, user_cfg)
    return cfg
