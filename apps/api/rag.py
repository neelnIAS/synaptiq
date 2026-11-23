"""Document text extraction and optional vector search helpers.

For semantic search, create a Supabase table named document_chunks with:
id uuid primary key default gen_random_uuid(),
user_id uuid, document_name text, content text, embedding vector(384).
Enable pgvector in Supabase before using vector search.
"""
from pypdf import PdfReader
from pathlib import Path

def extract_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()

def split_text(text: str, chunk_size: int = 900, overlap: int = 120):
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + chunk_size])
        start += chunk_size - overlap
    return [c for c in chunks if c.strip()]
