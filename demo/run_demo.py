from __future__ import annotations

from irl.core.pipeline import apply_irl


def main() -> None:
    user_query = "Use current standings. What is Detroit's most difficult game left?"
    # Intentionally flawed draft to demonstrate IRL catching a structural invariant violation.
    llm_draft = (
        "The Lions' toughest remaining game is probably vs the Steelers. "
        "The Bears game might not occur since it is currently not scheduled."
    )

    print("=== User Query ===")
    print(user_query)
    print("\n=== Raw LLM Draft ===")
    print(llm_draft)

    result = apply_irl(user_query, llm_draft)

    print("\n=== IRL Output ===")
    print(result.final_answer)

    print("\n=== IRL Metadata ===")
    print(f"domain: {result.domain}")
    print(f"invariant_passed: {result.invariant_passed}")
    if result.notes:
        print("notes:")
        for n in result.notes:
            print(f" - {n}")


if __name__ == "__main__":
    main()
