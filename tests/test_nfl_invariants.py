from irl.core.pipeline import apply_irl


def test_nfl_invariant_blocks_division_game_nonexistence():
    user_query = "Use current standings. Lions schedule?"
    llm_draft = "The Bears game might not occur since it is currently not scheduled."
    result = apply_irl(user_query, llm_draft)
    assert result.domain == "nfl_schedule"
    assert result.invariant_passed is False
    assert "Divisional opponents play twice" in result.notes[0]
