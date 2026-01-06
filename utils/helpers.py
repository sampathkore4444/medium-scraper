import re


def sanitize_filename(name: str) -> str:
    """Remove invalid Windows filename characters."""
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip()


def to_freedium_url(url: str) -> str:
    """Convert Medium URL to Freedium mirror."""
    if "freedium.cfd" in url:
        return url
    if "medium.com" not in url:
        raise ValueError("Please provide a valid Medium URL.")
    return f"https://freedium-mirror.cfd/{url}"
