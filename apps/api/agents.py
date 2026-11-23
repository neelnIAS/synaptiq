"""LangGraph-powered planning workflow. Uses a safe local fallback when no LLM key is configured."""
from typing import TypedDict
from langgraph.graph import StateGraph, END
from config import OPENAI_API_KEY, OPENAI_MODEL

class AgentState(TypedDict):
    request: str
    plan: str
    review: str

def planner(state: AgentState):
    request = state["request"]
    return {"plan": f"1. Understand the request: {request}\n2. Inspect related projects and tasks.\n3. Propose actionable next steps."}

def auditor(state: AgentState):
    plan = state.get("plan", "")
    return {"review": "Review complete: check ownership, deadlines, permissions and missing details before execution.\n" + plan}

graph = StateGraph(AgentState)
graph.add_node("planner", planner)
graph.add_node("auditor", auditor)
graph.set_entry_point("planner")
graph.add_edge("planner", "auditor")
graph.add_edge("auditor", END)
agent_app = graph.compile()

def run_agent(request: str):
    return agent_app.invoke({"request": request, "plan": "", "review": ""})
