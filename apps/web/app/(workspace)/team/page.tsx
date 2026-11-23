"use client";
import {useEffect,useState} from "react";
import {createClient} from "../../../src/utils/supabase/client";
export default function TeamPage(){
 const supabase=createClient();const [members,setMembers]=useState<any[]>([]);const [name,setName]=useState("");const [email,setEmail]=useState("");const [role,setRole]=useState("Member");const [message,setMessage]=useState("");
 async function load(){const {data,error}=await supabase.from("team_members").select("*").order("created_at",{ascending:false});if(error)setMessage(error.message);setMembers(data||[]);}
 useEffect(()=>{load()},[]);
 async function add(){const {error}=await supabase.from("team_members").insert({name,email,role});setMessage(error?.message||"Member added");if(!error){setName("");setEmail("");setRole("Member");load();}}
 async function remove(id:string){const {error}=await supabase.from("team_members").delete().eq("id",id);setMessage(error?.message||"Member removed");load();}
 return <main><h1>Team management</h1><section className="panel"><input placeholder="Name" value={name} onChange={e=>setName(e.target.value)}/><input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)}/><input placeholder="Role" value={role} onChange={e=>setRole(e.target.value)}/><button onClick={add}>Add member</button><p>{message}</p></section>{members.map(m=><section className="panel" key={m.id}><b>{m.name}</b><p>{m.email} · {m.role}</p><button className="secondary" onClick={()=>remove(m.id)}>Remove</button></section>)}</main>;
}
