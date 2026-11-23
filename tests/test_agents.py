from apps.api.agents import run_agent

def test_agent_returns_plan_and_review():
    result = run_agent("Prepare a project launch")
    assert result["plan"]
    assert result["review"]
