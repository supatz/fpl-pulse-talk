"""Last-action groupings for Understat shots — reusable map + site ? copy."""

from __future__ import annotations

# Canonical group order for legends / UI
LAST_ACTION_GROUP_ORDER = [
    "Combination play",
    "Through ball",
    "Crosses",
    "Dribble",
    "Turnover",
    "Second ball",
    "Unknown",
]

# Raw Understat lastAction → group
LAST_ACTION_TO_GROUP: dict[str, str] = {
    # Combination play — structured build-up pass before the shot
    "Pass": "Combination play",
    "LayOff": "Combination play",
    "HeadPass": "Combination play",
    # Through ball — line-breaking pass into space
    "Throughball": "Through ball",
    "Through ball": "Through ball",
    # Crosses — delivery from wide / floated ball
    "Cross": "Crosses",
    "Chipped": "Crosses",
    # Dribble — carrier beat a man or manipulated the ball
    "TakeOn": "Dribble",
    "GoodSkill": "Dribble",
    "BallTouch": "Dribble",
    # Turnover — shot after winning the ball back
    "BallRecovery": "Turnover",
    "Interception": "Turnover",
    "Tackle": "Turnover",
    "Challenge": "Turnover",
    "Dispossessed": "Turnover",
    # Second ball — chaotic / unintended second phase (incl. GK punches/saves)
    "Rebound": "Second ball",
    "Aerial": "Second ball",
    "Clearance": "Second ball",
    "BlockedPass": "Second ball",
    "Save": "Second ball",
    "Punch": "Second ball",
    # Unknown — missing or non-meaningful preceding action labels
    "None": "Unknown",
    "CornerAwarded": "Unknown",
    "Foul": "Unknown",
    "Goal": "Unknown",
    "End": "Unknown",
    "Card": "Unknown",
    "FormationChange": "Unknown",
    "KeeperPickup": "Unknown",
    "OffsidePass": "Unknown",
    "SubstitutionOn": "Unknown",
    "Standard": "Unknown",
}

GROUP_DEFINITIONS: dict[str, str] = {
    "Combination play": (
        "The shot followed a short or constructed pass (including lay-offs and headed "
        "passes). Reads as patterned build-up rather than a chaos or wide delivery."
    ),
    "Through ball": (
        "The chance was created by a pass that split the line and found a runner in space."
    ),
    "Crosses": (
        "The preceding action was a cross or chipped delivery, typically from wide areas "
        "into the box."
    ),
    "Dribble": (
        "The shooter (or carrier) created the chance by beating a defender or a skill/"
        "touch that opened the shot."
    ),
    "Turnover": (
        "The shot came after winning the ball — recovery, interception, tackle, challenge, "
        "or forcing a dispossess."
    ),
    "Second ball": (
        "The shot came from a chaotic second phase the attacker did not cleanly design: "
        "rebounds, aerials, clearances, blocked passes, or goalkeeper saves/punches that "
        "dropped to a shooter."
    ),
    "Unknown": (
        "No useful preceding action was recorded, or the label is administrative noise "
        "(e.g. none, foul, substitution) rather than how the chance was built."
    ),
}

# Shots on target for this product: goals, saves, and woodwork. Blocked shots excluded.
SOT_RESULTS = frozenset({"Goal", "SavedShot", "ShotOnPost"})


def last_action_group(raw: str | None) -> str:
    if raw is None or raw == "":
        return "Unknown"
    return LAST_ACTION_TO_GROUP.get(str(raw), "Unknown")


def groups_for_site() -> list[dict]:
    """Payload for serving JSON / ? tooltips."""
    members: dict[str, list[str]] = {g: [] for g in LAST_ACTION_GROUP_ORDER}
    for action, group in sorted(LAST_ACTION_TO_GROUP.items()):
        if action not in members[group]:
            members[group].append(action)
    return [
        {
            "group": g,
            "definition": GROUP_DEFINITIONS[g],
            "values": members[g],
        }
        for g in LAST_ACTION_GROUP_ORDER
    ]
