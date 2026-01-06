from fastapi import HTTPException
import os

TOKEN = os.getenv("TOKEN")


async def get_query_token(token: str):
    if token != TOKEN:
        raise HTTPException(status_code=400, detail="No LAMAS token provided")
