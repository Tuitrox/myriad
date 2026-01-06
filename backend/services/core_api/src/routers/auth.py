from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError, jwt
from jwt import decode, PyJWTError
import bcrypt
from datetime import datetime, timezone

from src.security import create_access_token, verify_turnstile
from src.database import get_db
from src.models import User
from src.schemas import UserRegisterRequest, UserResponse, Token
from src.config import settings
from src.rabbit import rabbit


router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)


async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    query = select(User).where(User.id == int(user_id))
    result = await db.execute(query)
    user = result.scalars().first()
    
    if user is None:
        raise credentials_exception
        
    return user


@router.post("/register")
async def register(user_data: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)

    is_valid = await verify_turnstile(user_data.captcha_token)
    if not is_valid:
        raise HTTPException(status_code=400, detail="CAPTCHA не пройдена!")
    
    if result.scalars().first():
        raise HTTPException(
            status_code=400, 
            detail="Пользователь с таким email уже существует"
        )

    hashed_pw = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw,
        is_active=True,
        is_verified=False
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token(data={"sub": new_user.email})
    
    message_body = {
        "type": "email_verification",
        "email": new_user.email,
        "token": token
    }
    
    await rabbit.send_task(
        queue_name="notifications_queue", 
        message_data=message_body
    )
    
    return {"status": "SUCCESS", "message": "Registration successful, email sending in background"}


@router.post("/verify")
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
        
    if user.is_verified:
        return {"message": "Already verified"}
    
    user.is_verified = True
    user.is_active = True
    await db.commit()
    
    return {"message": "Account verified successfully"}


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    query = select(User).where(User.email == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Пользователь не подтвердил почту."
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Пользователь был забанен."
        )

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user.last_login = datetime.now(timezone.utc)
    await db.commit()

    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}