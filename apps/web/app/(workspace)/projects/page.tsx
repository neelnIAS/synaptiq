"use client";
import {useEffect,useState} from "react";
import {createClient} from "../../../src/utils/supabase/client";
export default function ProjectsPage(){
 const supabase=createClient(); const [items,setItems]=useState<any[]>([]); const [name,setName]=useState(""); const [description,setDescription]=useState(""); const [message,setMessage]=useState("");
 async function load(){const {data,error}=await supabase.from("projects").select("*").order("created_at",{ascending:false}); if(error)setMessage(error.message); else setItems(data||[]);}
 useEffect(()=>{load();},[]);
 async function add(){const {data:{user}}=await supabase.auth.getUser(); if(!user){setMessage("Please log in first");return;} const {error}=await supabase.from("projects").insert({name,description,user_id:user.id}); if(error)setMessage(error.message);else{setName("");setDescription("");setMessage("Project created");load();}}
 async function remove(id:string){const {error}=await supabase.from("projects").delete().eq("id",id);setMessage(error?.message||"Project deleted");load();}
 return <main><h1>Projects</h1><section className="panel"><input placeholder="Project name" value={name} onChange={e=>setName(e.target.value)}/><input placeholder="Description" value={description} onChange={e=>setDescription(e.target.value)}/><button onClick={add}>Create project</button><p>{message}</p></section>{items.map(p=><section className="panel" key={p.id}><b>{p.name}</b><p>{p.description}</p><button className="secondary" onClick={()=>remove(p.id)}>Delete</button></section>)}</main>;
}
