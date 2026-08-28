"""Shot-zone derivation from Understat X/Y coordinates."""

from __future__ import annotations

from pipeline.understat.config import (
    ZONE_PENALTY_X,
    ZONE_PENALTY_Y_MAX,
    ZONE_PENALTY_Y_MIN,
    ZONE_SIX_YARD_X,
    ZONE_SIX_YARD_Y_MAX,
    ZONE_SIX_YARD_Y_MIN,
)


def shot_zone(x: float | None, y: float | None, *, result: str | None = None) -> str | None:
    """
    Map Understat pitch coords to zone labels aligned with their shotZone family.

    Returns: six_yard | penalty_area | outside_box | own_goal | None
    """
    if result == "OwnGoal":
        return "own_goal"
    if x is None or y is None:
        return None
    try:
        xf, yf = float(x), float(y)
    except (TypeError, ValueError):
        return None

    if xf >= ZONE_SIX_YARD_X and ZONE_SIX_YARD_Y_MIN <= yf <= ZONE_SIX_YARD_Y_MAX:
        return "six_yard"
    if xf >= ZONE_PENALTY_X and ZONE_PENALTY_Y_MIN <= yf <= ZONE_PENALTY_Y_MAX:
        return "penalty_area"
    return "outside_box"
