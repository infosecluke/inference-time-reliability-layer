from __future__ import annotations

from dataclasses import dataclass

from irl.core.router import detect_domain, Domain
from irl.core.claims import extract_claims
from irl.plugins.nfl.invariants import validate_nfl_invariants


@dataclass(frozen=True)
class IRLResult:
    final_answer: str
    domain: str
    invariant_passed: bool
    notes: list[str]


def apply_irl(user_query: str, draft: str) -> IRLResult:
    """Apply the IRL pipeline to an LLM draft (MVP).

    Behavior:
    - Detect NFL domain
    - Extract simple claims
    - Validate NFL invariants
    - If violated: rewrite output to correct the structural error + attach notes
    """
    decision = detect_domain(user_query, draft)

    if decision.domain != Domain.NFL_SCHEDULE:
        return IRLResult(
            final_answer=draft,
            domain=decision.domain.value,
            invariant_passed=True,
            notes=["IRL not applied (domain not structured in MVP)."],
        )

    claims = extract_claims(user_query, draft)
    report = validate_nfl_invariants(claims, draft)

    if report.passed:
        return IRLResult(
            final_answer=draft,
            domain=decision.domain.value,
            invariant_passed=True,
            notes=["Invariant checks passed."],
        )

    corrected = draft
    replacements = {
        "might not occur": "will occur (TBD time/date)",
        "may not occur": "will occur (TBD time/date)",
        "might not happen": "will happen (TBD time/date)",
        "may not happen": "will happen (TBD time/date)",
    }
    for k, v in replacements.items():
        corrected = corrected.replace(k, v)

    if corrected == draft:
        corrected = (
            draft.rstrip()
            + "\n\nCorrection: Divisional games occur twice every season; a TBD listing does not mean the game might not occur."
        )

    notes = [f"{v.code}: {v.message}" for v in report.violations]

    return IRLResult(
        final_answer=corrected,
        domain=decision.domain.value,
        invariant_passed=False,
        notes=notes,
    )
