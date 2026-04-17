from math import ceil


def calculate_pages(total_items: int, limit: int) -> int:
    return ceil(total_items / limit) if limit > 0 else 0
