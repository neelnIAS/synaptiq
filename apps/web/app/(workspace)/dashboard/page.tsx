"use client";
import { useEffect, useState } from "react";
import { createClient } from "../../../src/utils/supabase/client";
export default function DashboardPage() {
  const supabase = createClient();
  const [projects, setProjects] = useState<any[]>([]);
  const [tasks, setTasks] = useState<any[]>([]);
  useEffect(() => {
    (async () => {
      const { data: p } = await supabase.from("projects").select("*"); setProjects(p || []);
      const { data: t } = await supabase.from("tasks").select("*"); setTasks(t || []);
    })();
  }, []);
  const done = tasks.filter(t => t.status === "done").length;
  return <main><h1>Dashboard</h1><div className="grid">
    <div className="panel"><small>Total projects</small><h2>{projects.length}</h2></div>
    <div className="panel"><small>Total tasks</small><h2>{tasks.length}</h2></div>
    <div className="panel"><small>Completed tasks</small><h2>{done}</h2></div>
    <div className="panel"><small>Pending tasks</small><h2>{tasks.length - done}</h2></div>
  </div><section className="panel"><h2>Project progress</h2>{projects.map(p => { const related = tasks.filter(t => t.project_id === p.id); const percent = related.length ? Math.round(related.filter(t => t.status === "done").length / related.length * 100) : 0; return <p key={p.id}>{p.name} — {percent}% ({related.length} tasks)</p>; })}</section></main>;
}
