# django-media-service

Reusable Django app for private media upload, thumbnail generation, and HLS processing.

## Installation

```bash
pip install git+ssh://git@github.com/dr-baka/django-media-service.git
```

## Setup

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "rest_framework",
    "django_media_service",
]
```

Include URLs:

```python
from django.urls import include, path
urlpatterns = [
    path("", include("django_media_service.urls")),
]
```

## Celery (RabbitMQ)

```python
CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
```

## Settings

Use `DJANGO_MEDIA_SERVICE` override in Django settings (see `django_media_service/settings.py` defaults).

## Upload flow

1. `POST /api/media/presign-upload/`
2. Upload directly to MinIO using returned URL.
3. `POST /api/media/confirm-upload/`
4. Async tasks run for metadata/thumbnail/HLS.

## Example payload

```json
{
  "filename": "video.mp4",
  "mime_type": "video/mp4",
  "file_size": 10485760,
  "thumbnail_enabled": true,
  "hls_enabled": true,
  "is_private": true
}
```

## ffmpeg dependency

Install system ffmpeg binary in runtime environment.
