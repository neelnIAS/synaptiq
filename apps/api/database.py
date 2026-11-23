import httpx
from fastapi import HTTPException
from config import SUPABASE_URL, SUPABASE_ANON_KEY

def headers(token: str):
    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

async def request_table(method: str, table: str, token: str, params=None, body=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.request(method, url, headers=headers(token), params=params, json=body)
    if response.status_code >= 400:
        try:
            detail = response.json()
        except Exception:
            detail = response.text
        raise HTTPException(status_code=response.status_code, detail=detail)
    if response.status_code == 204 or not response.text:
        return None
    return response.json()
