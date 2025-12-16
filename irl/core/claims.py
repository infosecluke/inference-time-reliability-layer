from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ClaimType(str, Enum):
    SCHEDULE_EXISTENCE = "schedule_existence"
    OTHER = "other"


@dataclass(frozen=True)
class Claim:
    type: ClaimType
    subject: str
    opponent: str | None = None
    season: int | None = None
    raw: str | None = None
    meta: dict[str, Any] | None = None


def extract_claims(user_query: str, draft: str) -> list[Claim]:
    """Minimal claim extraction (MVP).

    We keep this deliberately simple for clarity. In production,
    use constrained extraction to a JSON schema or an IE model.
    """
    text = (user_query + " " + draft).lower()
    claims: list[Claim] = []

    # Demo: if Lions and Bears appear together, assume a schedule-existence claim.
    if "lions" in text and "bears" in text:
        claims.append(
            Claim(
                type=ClaimType.SCHEDULE_EXISTENCE,
                subject="DET",
                opponent="CHI",
                season=2025,
                raw="Lions vs Bears game existence",
            )
        )

    if not claims:
        claims.append(Claim(type=ClaimType.OTHER, subject="unknown", raw=draft))

    return claims
