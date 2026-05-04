class MediaType:
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    OTHER = "other"

    CHOICES = [
        (IMAGE, "Image"),
        (VIDEO, "Video"),
        (AUDIO, "Audio"),
        (DOCUMENT, "Document"),
        (OTHER, "Other"),
    ]


class ProcessingStatus:
    DISABLED = "disabled"
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"

    CHOICES = [
        (DISABLED, "Disabled"),
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (READY, "Ready"),
        (FAILED, "Failed"),
    ]
