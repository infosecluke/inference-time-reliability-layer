from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Domain(str, Enum):
    NFL_SCHEDULE = "nfl_schedule"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class DomainDecision:
    domain: Domain
    confidence: float


def detect_domain(user_query: str, draft: str | None = None) -> DomainDecision:
    """High-precision domain router (MVP).

    For the demo, we trigger on a few NFL schedule/standings tokens.
    In production, replace with a classifier + entity recognition.
    """
    text = f"{user_query} {draft or ''}".lower()
    triggers = [
        "lions", "bears", "packers", "vikings",
        "week 18", "week 17", "schedule", "standings", "playoff"
    ]
    if any(t in text for t in triggers):
        return DomainDecision(domain=Domain.NFL_SCHEDULE, confidence=0.85)
    return DomainDecision(domain=Domain.UNKNOWN, confidence=0.2)
