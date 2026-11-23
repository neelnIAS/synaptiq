"""Small tool layer used by the AI workflow. These functions call the same API data layer."""
from database import request_table

async def list_projects(token: str, user_id: str):
    return await request_table("GET", "projects", token, {"select": "*", "user_id": f"eq.{user_id}", "order": "created_at.desc"})

async def list_tasks(token: str, project_id: str | None = None):
    params = {"select": "*", "order": "created_at.desc"}
    if project_id:
        params["project_id"] = f"eq.{project_id}"
    return await request_table("GET", "tasks", token, params)
