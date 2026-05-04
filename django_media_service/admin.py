from django.contrib import admin
from .models import MediaAsset
from .tasks.media_tasks import generate_hls, generate_thumbnails, cleanup_media_files

@admin.action(description="Reprocess thumbnail")
def reprocess_thumbnail(modeladmin, request, queryset):
    for o in queryset: generate_thumbnails.delay(str(o.id))

@admin.action(description="Reprocess HLS")
def reprocess_hls(modeladmin, request, queryset):
    for o in queryset: generate_hls.delay(str(o.id))

@admin.action(description="Cleanup files")
def cleanup_files(modeladmin, request, queryset):
    for o in queryset: cleanup_media_files.delay(str(o.id))

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("id", "original_filename", "media_type", "owner", "file_size", "thumbnail_status", "hls_status", "created_at")
    list_filter = ("media_type", "thumbnail_status", "hls_status", "is_private")
    actions = [reprocess_thumbnail, reprocess_hls, cleanup_files]
