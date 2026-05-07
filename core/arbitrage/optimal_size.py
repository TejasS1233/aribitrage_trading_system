import math


def calculate_optimal_volume(legs: list[dict[str, float]], fee: float = 0.001) -> float:
    """Calculate optimal trade volume constrained by order book depth."""
    if not legs:
        return 0.001

    min_volume = float("inf")
    for leg in legs:
        bid_vol = leg.get("bid_volume", 0)
        ask_vol = leg.get("ask_volume", 0)
        min_volume = min(min_volume, bid_vol, ask_vol)

    optimal = min_volume * 0.5
    return max(optimal, 0.001)
