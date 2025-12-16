from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from irl.core.claims import Claim, ClaimType


@dataclass(frozen=True)
class InvariantViolation:
    code: str
    message: str
    claim_raw: str | None = None


@dataclass(frozen=True)
class InvariantReport:
    passed: bool
    violations: list[InvariantViolation]


def validate_nfl_invariants(claims: Iterable[Claim], draft: str) -> InvariantReport:
    """NFL structural invariants (demo subset).

    MVP invariant:
    - Do not claim a division game might/may not occur merely because time/date is TBD.
      (Divisional opponents play twice every regular season.)

    For the demo, we detect the bad pattern: "might not occur" / "may not occur" etc.
    when the claim is DET vs CHI.
    """
    text = draft.lower()
    violations: list[InvariantViolation] = []

    for c in claims:
        if c.type == ClaimType.SCHEDULE_EXISTENCE and c.subject == "DET" and c.opponent == "CHI":
            bad_phrases = ["might not occur", "may not occur", "may not happen", "might not happen"]
            if any(p in text for p in bad_phrases):
                violations.append(
                    InvariantViolation(
                        code="NFL_DIVISION_GAME_EXISTENCE",
                        message=(
                            "Divisional opponents play twice every season; "
                            "a TBD listing does not imply the game might not occur."
                        ),
                        claim_raw=c.raw,
                    )
                )

    return InvariantReport(passed=(len(violations) == 0), violations=violations)
