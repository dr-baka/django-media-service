class MediaServiceError(Exception):
    pass


class ValidationError(MediaServiceError):
    pass


class StorageError(MediaServiceError):
    pass


class ProcessingError(MediaServiceError):
    pass
