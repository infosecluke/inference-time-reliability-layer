# Inference-Time Reliability Layer (IRL)

Large language models occasionally produce errors that violate **basic structural rules** of well-defined domains (e.g., sports schedules, finance, calendars, time zones). These are not subtle factual disagreements but **structural invariant violations**—statements that should be impossible.

This repository presents an **Inference-Time Reliability Layer (IRL)**: a thin, inference-time system component that enforces domain invariants, performs selective verification, and gates confidence before responses reach users.

---

## Motivation

Many trust-damaging LLM errors are **systems failures**, not training failures.

Examples include:
- Treating “TBD” scheduling as “might not occur”
- Violating conservation rules (e.g., wins + losses ≠ games played)
- Producing logically impossible calendar or timezone claims

These failures disproportionately erode user trust and are often best addressed through **deterministic validation at inference time**, rather than:
- additional model training,
- unsafe self-learning loops, or
- overgeneralized prompt constraints.

---

## Core Idea

The IRL sits **between draft generation and final response**.

It does not make models “smarter.”  
It makes them **structurally reliable** in domains where correctness is cheap to verify.

Key principles:
- Enforce invariants where they exist
- Verify selectively where authoritative data is cheap
- Prefer uncertainty over confident impossibility
- Minimize blast radius and latency

---

## Architecture Overview

```mermaid
flowchart LR
    U[User Query] --> M[LLM Draft Response]

    M --> D[Domain Detection]
    D -->|Structured Domain| C[Claim Extraction]
    D -->|Unstructured Domain| F[Final Response]

    C --> I[Invariant Validation]
    I -->|Violation| R[Draft Revision / Fallback]
    R --> M

    I -->|Pass| V[Selective Verification]
    V --> G[Confidence Gating]
'''

    G --> F[Final Response]
    F --> L[Logging & Evals]
