import mimetypes

def detect_media_type(mime_type: str) -> str:
    if mime_type.startswith("image/"): return "image"
    if mime_type.startswith("video/"): return "video"
    if mime_type.startswith("audio/"): return "audio"
    if mime_type in ("application/pdf",) or mime_type.startswith("application/"): return "document"
    return "other"

def get_extension(filename: str) -> str:
    return (mimetypes.guess_extension(filename) or "").replace(".", "")
