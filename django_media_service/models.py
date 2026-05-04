import uuid
from django.conf import settings
from django.db import models
from .constants import MediaType, ProcessingStatus


class MediaAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    original_filename = models.CharField(max_length=255)
    file_key = models.CharField(max_length=1024)
    bucket_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    extension = models.CharField(max_length=32, blank=True)
    file_size = models.BigIntegerField()
    media_type = models.CharField(max_length=20, choices=MediaType.CHOICES, default=MediaType.OTHER)
    is_private = models.BooleanField(default=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    thumbnail_enabled = models.BooleanField(default=False)
    thumbnail_status = models.CharField(max_length=20, choices=ProcessingStatus.CHOICES, default=ProcessingStatus.DISABLED)
    thumbnail_data = models.JSONField(default=dict, blank=True)
    hls_enabled = models.BooleanField(default=False)
    hls_status = models.CharField(max_length=20, choices=ProcessingStatus.CHOICES, default=ProcessingStatus.DISABLED)
    hls_data = models.JSONField(default=dict, blank=True)
    processing_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
