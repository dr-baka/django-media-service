from django.utils.module_loading import import_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from ..models import MediaAsset
from ..settings import get_config
from ..tasks.media_tasks import process_metadata, generate_thumbnails, generate_hls, cleanup_media_files
from ..services.upload_service import validate_upload, create_presign
from ..services.media_service import create_asset
from ..services.url_service import sign_get_url
from ..storage import get_storage_client
from .serializers import MediaAssetSerializer, PresignUploadSerializer, ConfirmUploadSerializer


class MediaAssetViewSet(viewsets.ModelViewSet):
    serializer_class = MediaAssetSerializer
    queryset = MediaAsset.objects.all()
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        perm_path = get_config()["PERMISSIONS"]["DEFAULT_PERMISSION_CLASS"]
        return [import_string(perm_path)()]

    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user
        if u.is_staff or u.is_superuser:
            return qs
        return qs.filter(owner=u)

    @action(detail=False, methods=["post"], url_path="presign-upload")
    def presign_upload(self, request):
        s = PresignUploadSerializer(data=request.data); s.is_valid(raise_exception=True)
        d = s.validated_data
        validate_upload(d["mime_type"], d["file_size"])
        file_key, url = create_presign(d["filename"], d["mime_type"])
        return Response({"file_key": file_key, "upload_url": url})

    @action(detail=False, methods=["post"], url_path="confirm-upload")
    def confirm_upload(self, request):
        s = ConfirmUploadSerializer(data=request.data); s.is_valid(raise_exception=True)
        d = s.validated_data
        if not get_storage_client().object_exists(d["file_key"]):
            return Response({"detail": "object not found"}, status=400)
        asset = create_asset(request.user if request.user.is_authenticated else None, d["filename"], d["file_key"], d["mime_type"], d["file_size"], d.get("thumbnail_enabled", False), d.get("hls_enabled", False), d.get("is_private", True))
        process_metadata.delay(str(asset.id))
        if asset.thumbnail_enabled: generate_thumbnails.delay(str(asset.id))
        if asset.hls_enabled and asset.media_type == "video": generate_hls.delay(str(asset.id))
        return Response(MediaAssetSerializer(asset).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="upload")
    def upload(self, request):
        f = request.FILES["file"]
        asset = create_asset(request.user if request.user.is_authenticated else None, f.name, f"media/tmp/{f.name}", f.content_type or "application/octet-stream", f.size)
        return Response(MediaAssetSerializer(asset).data, status=201)

    @action(detail=True, methods=["post"], url_path="signed-url")
    def signed_url(self, request, pk=None):
        asset = self.get_object()
        return Response({"url": sign_get_url(asset.file_key)})

    @action(detail=True, methods=["post"], url_path="process-thumbnail")
    def process_thumbnail(self, request, pk=None):
        generate_thumbnails.delay(pk)
        return Response({"status": "queued"})

    @action(detail=True, methods=["post"], url_path="process-hls")
    def process_hls(self, request, pk=None):
        generate_hls.delay(pk)
        return Response({"status": "queued"})

    @action(detail=True, methods=["get"], url_path="hls/signed-playback")
    def hls_signed_playback(self, request, pk=None):
        asset = self.get_object()
        data = asset.hls_data or {}
        out = {"master": sign_get_url(data.get("master")) if data.get("master") else None, "variants": {}}
        for name, v in data.get("variants", {}).items():
            out["variants"][name] = {"playlist": sign_get_url(v["playlist"])}
        return Response(out)

    def perform_destroy(self, instance):
        cleanup_media_files.delay(str(instance.id))
        instance.delete()
