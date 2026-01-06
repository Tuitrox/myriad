from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.database import Base

# --- ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True) 
    last_login = Column(DateTime(timezone=True), nullable=True)

    notes = relationship("Note", back_populates="owner")


# --- ТАБЛИЦА ЗАМЕТОК ---
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    text = Column(Text, nullable=False)
    
    tags = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    
    is_processed = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="notes")