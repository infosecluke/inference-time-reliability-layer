# Inference-Time Reliability Layer (IRL)
## A Practical Proposal for Eliminating Structural Errors in Large Language Models

### Executive Summary
Large language models still produce occasional errors that users experience as “careless” or “silly.” These are not subtle factual disagreements but violations of basic structural rules in well-defined domains.

## IRL Architecture Overview

```mermaid
flowchart LR
    U[User Query] --> M[LLM Draft Response]
    M --> D[Domain Detection]
    D -->|Structured Domain| C[Claim Extraction]
    D -->|Unstructured Domain| F[Final Response]
    C --> I[Invariant Validation]
    I -->|Violation| R[Draft Revision]
    R --> M
    I -->|Pass| V[Selective Verification]
    V --> G[Confidence Gating]
    G --> F[Final Response]
    F --> L[Logging & Evals]


Example: implying that an NFL divisional game “might not occur” because its Week 18 time is TBD. Divisional opponents play twice every season. The game’s time may be unknown; the game itself is guaranteed.

This proposal argues that these failures are not training problems. They are systems problems. The most direct fix is an inference-time Reliability Layer that enforces domain invariants, performs selective verification, and gates confidence.

---

## The Problem: Structural Errors That Should Be Impossible
These errors:
1. Violate deterministic rules
2. Instantly erode trust among domain experts
3. Are highly preventable
4. Cause disproportionate reputational damage

Calling them “hallucinations” obscures the root cause. The model is not inventing facts; it is failing to respect constraints.

---

## Core Insight
This is not an intelligence problem.  
**It is a missing validation layer problem.**

Training improves probability. Structural correctness requires enforcement.

---

## Proposed Solution: Inference-Time Reliability Layer (IRL)

The IRL sits between draft generation and final response.

**Pipeline**
1. Draft generation
2. Domain detection and routing
3. Claim extraction
4. Invariant validation
5. Selective verification retrieval
6. Confidence gating and language control
7. Final response + logging

---

## Domain Detection
Activated only for domains with strong structure and cheap verification:
- Sports schedules and standings
- Finance quotes and earnings
- Weather and time zones
- Calendar logic
- Math and unit conversions

High precision is favored to minimize latency.

---

## Claim Extraction
The system extracts structured assertions rather than validating prose:
- Entities (teams, dates, records)
- Predicates (“will play”, “eliminated”)
- Quantitative claims

This enables deterministic validation.

---

## Invariant Validation (Hard Rules)
Invariant checks enforce rules that should never be violated.

**NFL examples**
- Divisional opponents play two games every regular season
- TBD scheduling ≠ non-occurrence
- Week 18 always exists
- Wins + losses + ties = games played

Violations block the draft and force revision.

---

## Selective Verification Retrieval
Where authoritative data exists:
- Retrieve only required fields
- Prefer league or primary sources
- Cache short-lived results
- Reconcile contradictions deterministically

If retrieval fails, certainty is downgraded rather than guessed.

---

## Confidence Gating
- Invariant-backed claims may be stated confidently
- Unverified claims must be hedged
- “Unknown” is always preferable to “confidently wrong”

---

## Operational Feedback Loop
Incident → invariant violation → logging → eval addition → rule refinement

This enables durable reliability improvements without unsafe self-training from user text.

---

## Why This Works
- High leverage against trust-damaging errors
- No retraining required
- Resistant to poisoning
- Auditable and reversible
- Scales by focusing on structured domains

---

## Implementation Roadmap
**Phase 1:** NFL pilot  
**Phase 2:** Expand to other structured domains  
**Phase 3:** Generalize invariant tooling  

---

## Metrics
- Invariant violation rate
- Verified contradiction rate
- Overconfidence reduction
- User trust signals

---

## Conclusion
Preventing structurally impossible errors at inference time is one of the most practical ways to advance trustworthy AI. This approach complements training and improves reliability through sound systems engineering.
