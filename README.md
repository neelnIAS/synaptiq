# Synaptiq

AI-assisted project and task management workspace.

## Project layout
- `apps/api`: FastAPI backend, Supabase REST access, document extraction and LangGraph workflow.
- `apps/web`: Next.js frontend.
- `tests`: starter tests.
- `.github/workflows`: basic Python compile CI.

## 1. Supabase setup

Create tables in Supabase SQL Editor:

```sql
create extension if not exists pgcrypto;

create table if not exists projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name varchar(150) not null,
  description text,
  created_at timestamptz default now()
);

create table if not exists team_members (
  id uuid primary key default gen_random_uuid(),
  name varchar(100) not null,
  email varchar(150) unique not null,
  role varchar(100) default 'Member',
  created_at timestamptz default now()
);

create table if not exists tasks (
  id uuid primary key default gen_random_uuid(),
  project_id uuid not null references projects(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  title varchar(250) not null,
  priority varchar(10) default 'medium' check (priority in ('low','medium','high')),
  status varchar(20) default 'todo' check (status in ('todo','in_progress','done')),
  assigned_to uuid references team_members(id) on delete set null,
  created_at timestamptz default now()
);

alter table projects enable row level security;
alter table tasks enable row level security;
alter table team_members enable row level security;

create policy "Users manage own projects" on projects for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "Users manage own tasks" on tasks for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "Authenticated users read team" on team_members for select to authenticated using (true);
create policy "Authenticated users manage team" on team_members for all to authenticated using (true) with check (true);
```

If you already created these tables, compare columns and add only missing columns, for example:
`alter table tasks add column if not exists assigned_to uuid references team_members(id) on delete set null;`

## 2. Backend setup

Copy `apps/api/.env.example` to `apps/api/.env` and fill in your Supabase URL and anon key.

Windows PowerShell:
```powershell
cd apps/api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## 3. Frontend setup

Copy `apps/web/.env.local.example` to `apps/web/.env.local` and fill in the same Supabase URL and anon key.

```powershell
cd apps/web
npm install
npm run dev
```

Open `http://localhost:3000`.

## Notes about advanced features

- PDF extraction and chunk splitting are implemented. Persisting embeddings and retrieval-augmented generation require a `document_chunks` table, pgvector, an embedding model and an indexing workflow; this starter does not silently claim those are configured.
- The LangGraph planner/auditor graph is implemented as a deterministic workflow. Connect an LLM provider and add approval-gated tool execution before allowing agents to modify production data.
- `/ai/stream` demonstrates SSE response delivery. It is not token-by-token LLM streaming yet.
- For production, add per-user ownership to team members, stricter RLS policies, rate limiting, audit logs, secure upload limits, and comprehensive tests.
