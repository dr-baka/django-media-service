def generate_for_asset(asset, bitrates):
    variants = {name: {"playlist": f"media/{asset.id}/hls/{name}/index.m3u8"} for name in bitrates.keys()}
    return {"master": f"media/{asset.id}/hls/master.m3u8", "variants": variants}
