from pydantic import BaseModel
from typing import Optional, List

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    user: "UserResponse"

class UserResponse(BaseModel):
    id: int
    username: str
    real_name: str
    role: Optional[str] = None
    permissions: List[str] = []
    
    class Config:
        from_attributes = True

class CurrentUserResponse(BaseModel):
    id: int
    username: str
    real_name: str
    department: Optional[str]
    role: str
    permissions: List[str]
    
    class Config:
        from_attributes = True

LoginResponse.model_rebuild()
