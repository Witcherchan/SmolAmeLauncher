"""
Formatting utility functions.
"""


def format_playtime(seconds: float) -> str:
    """Convert seconds into a human-readable string like '1h 4m 22s'."""
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")

    return " ".join(parts)


def truncate_label(text: str, max_chars: int = 12, suffix: str = "...") -> str:
    """Truncate text with a suffix if it exceeds max_chars."""
    if len(text) > max_chars:
        return text[:max_chars] + suffix
    return text
