"use client";
import {useEffect,useState} from "react";
export default function ApiTest(){const [status,setStatus]=useState("Checking...");useEffect(()=>{fetch(`${process.env.NEXT_PUBLIC_API_URL||"http://127.0.0.1:8000"}/health`).then(r=>r.json()).then(d=>setStatus(d.status)).catch(e=>setStatus(e.message));},[]);return <main><section className="panel"><h1>API connection test</h1><p>Backend status: {status}</p></section></main>}
