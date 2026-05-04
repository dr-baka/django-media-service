def generate_for_asset(asset):
    return {"small": f"media/{asset.id}/thumbnails/small.jpg", "medium": f"media/{asset.id}/thumbnails/medium.jpg", "large": f"media/{asset.id}/thumbnails/large.jpg"}
