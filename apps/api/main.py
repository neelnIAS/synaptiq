
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import os
import httpx
from typing import Optional, Literal
from pydantic import BaseModel
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from auth import verify_token, security
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Synaptiq API")


# Allowed frontend addresses
origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Synaptiq",
        "status": "Backend is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/protected")
def protected_route(user=Depends(verify_token)):
    return {
        "message": "Authentication successful!",
        "user_id": user.get("sub"),
        "email": user.get("email")
    }


# Project input model
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None


# Supabase request headers
def get_supabase_headers(token):
    key = os.getenv("SUPABASE_ANON_KEY")

    if not key:
        raise HTTPException(
            status_code=500,
            detail="Supabase publishable key is missing"
        )

    return {
        "apikey": key,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }


# Get all projects belonging to logged-in user
@app.get("/projects")
async def get_projects(
    user=Depends(verify_token),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    url = f"{os.getenv('SUPABASE_URL')}/rest/v1/projects"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params={"select": "*"},
            headers=get_supabase_headers(credentials.credentials)
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Unable to retrieve projects"
        )

    return response.json()


# Create a new project
@app.post("/projects")
async def create_project(
    project: ProjectCreate,
    user=Depends(verify_token),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    url = f"{os.getenv('SUPABASE_URL')}/rest/v1/projects"

    project_data = {
        "title": project.title,
        "description": project.description,
        "user_id": user["sub"]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=project_data,
            headers=get_supabase_headers(credentials.credentials)
        )

    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()


# Project update model
class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# PATCH: Update project
@app.patch("/projects/{project_id}")
async def update_project(
    project_id: str,
    project: ProjectUpdate,
    user=Depends(verify_token),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    update_data = project.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Please provide project details"
        )

    url = f"{os.getenv('SUPABASE_URL')}/rest/v1/projects"

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            url,
            params={"id": f"eq.{project_id}"},
            json=update_data,
            headers=get_supabase_headers(credentials.credentials)
        )

    if response.status_code not in (200, 204):
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return {"message": "Project updated successfully"}


# DELETE: Delete project
@app.delete("/projects/{project_id}")
async def delete_project(
    project_id: str,
    user=Depends(verify_token),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    url = f"{os.getenv('SUPABASE_URL')}/rest/v1/projects"

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            url,
            params={"id": f"eq.{project_id}"},
            headers=get_supabase_headers(credentials.credentials)
        )

    if response.status_code not in (200, 204):
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return {"message": "Project deleted successfully"}


# =====================================
# TASK MANAGEMENT
# =====================================

# Task input model
class TaskCreate(BaseModel):
    project_id: str
    title: str
    priority: Literal["low", "medium", "high"] = "medium"
    status: Literal["todo", "in_progress", "done"] = "todo"
    assigned_to: Optional[str] = None


# Task update model
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = None
    assigned_to: Optional[str] = None


# GET: Retrieve tasks
@app.get("/tasks")
async def get_tasks(
    project_id: Optional[str] = None,
    user=Depends(verify_token),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    url = f"{os.getenv('SUPABASE_URL')}/rest/v1/tasks"

    params = {
        "select": "*",
        "order": "created_at.desc"
    }

    if project_id:
        params["project_id"] = f"eq.{project_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            params=params,
            headers=get_supabase_headers(credentials.credentials)
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Unable to retrieve tasks"
        )

    return response.json()


# POST: Create a task
@app.post("/tasks")
async def create_task(
    task: TaskCreate,
    user=Depends(verify_token),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    url = f"{os.getenv('SUPABASE_URL')}/rest/v1/tasks"

    task_data = {
        "project_id": task.project_id,
        "user_id": user["sub"],
        "title": task.title,
        "priority": task.priority,
        "status": task.status,
        "assigned_to": task.assigned_to
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=task_data,
            headers=get_supabase_headers(credentials.credentials)
        )

    if response.status_code not in (200, 201):
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return response.json()


# PATCH: Update a task
@app.patch("/tasks/{task_id}")
async def update_task(
    task_id: str,
    task: TaskUpdate,
    user=Depends(verify_token),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    update_data = task.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Please provide at least one field to update"
        )

    url = f"{os.getenv('SUPABASE_URL')}/rest/v1/tasks"

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            url,
            params={"id": f"eq.{task_id}"},
            json=update_data,
            headers=get_supabase_headers(credentials.credentials)
        )

    if response.status_code not in (200, 204):
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return {"message": "Task updated successfully"}


# DELETE: Delete a task
@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: str,
    user=Depends(verify_token),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    url = f"{os.getenv('SUPABASE_URL')}/rest/v1/tasks"

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            url,
            params={"id": f"eq.{task_id}"},
            headers=get_supabase_headers(credentials.credentials)
        )

    if response.status_code not in (200, 204):
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return {"message": "Task deleted successfully"}
