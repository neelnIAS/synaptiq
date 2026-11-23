"use client";
import { useState } from "react";
import { createClient } from "../../../src/utils/supabase/client";
export default function DocumentsPage() {
    const supabase = createClient(); const [file, setFile] = useState<File | null>(null); const [result, setResult] = useState("");
    async function upload() { if (!file) return; const { data } = await supabase.auth.getSession(); const form = new FormData(); form.append("file", file); const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/documents/extract`, { method: "POST", headers: { Authorization: `Bearer ${data.session?.access_token || ""}` }, body: form }); const json = await response.json(); setResult(response.ok ? `Extracted ${json.characters} characters from ${json.filename}. ${json.chunks?.length || 0} chunks created.` : JSON.stringify(json.detail)); }
    return <main><h1>Document intelligence</h1><section className="panel"><p>Upload a PDF to extract text and split it into chunks for a future vector-search workflow.</p><input type="file" accept="application/pdf" onChange={e => setFile(e.target.files?.[0] || null)} /><button onClick={upload}>Extract PDF</button><p>{result}</p></section></main>;
}
