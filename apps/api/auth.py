from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import httpx
from config import SUPABASE_URL, SUPABASE_ANON_KEY

security = HTTPBearer(auto_error=False)

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing bearer token")
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {credentials.credentials}",
    }
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = response.json()
    return {"id": user["id"], "email": user.get("email"), "token": credentials.credentials}
