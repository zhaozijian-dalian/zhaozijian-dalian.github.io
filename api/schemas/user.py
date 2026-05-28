from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    real_name: str
    department: Optional[str] = None
    role_id: int

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    real_name: Optional[str] = None
    department: Optional[str] = None
    role_id: Optional[int] = None
    status: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    real_name: str
    department: Optional[str]
    role: Optional[str]
    status: str
    created_at: datetime
    last_login_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    total: int
    users: list[UserResponse]
