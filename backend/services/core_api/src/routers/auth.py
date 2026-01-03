from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt

from src.database import get_db
from src.models import User
from src.schemas import UserCreate, UserResponse


router = APIRouter(prefix="/auth", tags=["Auth"])


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    if result.scalars().first():
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )

    hashed_pw = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user