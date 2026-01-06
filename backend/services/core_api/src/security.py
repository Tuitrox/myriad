from datetime import datetime, timedelta, timezone
from jose import jwt
from src.config import settings

import httpx


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def verify_turnstile(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": settings.TURNSTILE_SECRET_KEY,
                "response": token
            }
        )
        result = response.json()
        return result.get("success", False)