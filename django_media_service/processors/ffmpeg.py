import ffmpeg


def probe(path: str):
    return ffmpeg.probe(path)
