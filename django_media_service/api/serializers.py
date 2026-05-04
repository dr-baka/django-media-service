from rest_framework import serializers
from ..models import MediaAsset


class MediaAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAsset
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")


class PresignUploadSerializer(serializers.Serializer):
    filename = serializers.CharField()
    mime_type = serializers.CharField()
    file_size = serializers.IntegerField()
    thumbnail_enabled = serializers.BooleanField(required=False)
    hls_enabled = serializers.BooleanField(required=False)
    is_private = serializers.BooleanField(required=False)


class ConfirmUploadSerializer(PresignUploadSerializer):
    file_key = serializers.CharField()
