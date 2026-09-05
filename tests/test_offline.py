from relay_desk.pipeline import run


def test_offline_pipeline_has_three_stages():
    result = run("Should an SMB buy an AI support bot this quarter?", offline_mode=True)
    assert result.mode == "offline"
    assert "Research" in result.research
    assert "Brief" in result.draft
    assert "Roast" in result.roast
    assert "support bot" in result.as_markdown().lower()
