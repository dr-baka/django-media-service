from PIL import Image


def create_thumbnail(src: str, dst: str, size: tuple[int, int]):
    with Image.open(src) as img:
        img.thumbnail(size)
        img.save(dst, format="JPEG")
