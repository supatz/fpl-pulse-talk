"""Name normalization for FPL ↔ Understat player matching."""

from __future__ import annotations

import html
import re
import unicodedata

_PUNCT = re.compile(r"[^a-z0-9\s]")
_SPACE = re.compile(r"\s+")
_TRANSLATE = str.maketrans(
    {
        "ø": "o",
        "Ø": "o",
        "ð": "d",
        "Ð": "d",
        "æ": "ae",
        "Æ": "ae",
        "ß": "ss",
        "ı": "i",
        "İ": "i",
        "ł": "l",
        "Ł": "l",
        "đ": "d",
        "Đ": "d",
    }
)


def strip_accents(value: str) -> str:
    nfkd = unicodedata.normalize("NFKD", value.translate(_TRANSLATE))
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def normalize_name(value: str | None) -> str:
    if value is None:
        return ""
    s = html.unescape(str(value))
    s = strip_accents(s).lower().replace("'", "").replace("`", "").replace(".", " ").replace("-", " ")
    s = _PUNCT.sub(" ", s)
    return _SPACE.sub(" ", s).strip()


def name_tokens(value: str | None) -> list[str]:
    n = normalize_name(value)
    return n.split() if n else []


def last_name(value: str | None) -> str:
    tokens = name_tokens(value)
    return tokens[-1] if tokens else ""


def first_initial(value: str | None) -> str:
    tokens = name_tokens(value)
    if not tokens:
        return ""
    return tokens[0][:1]


def full_name(first: str | None, second: str | None) -> str:
    return " ".join(p for p in (first or "", second or "") if p).strip()


def web_name_key(web_name: str | None) -> str:
    return normalize_name(web_name)
