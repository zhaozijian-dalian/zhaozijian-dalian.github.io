from sqlalchemy.orm import Session
from models import User
from schemas.auth import LoginRequest, LoginResponse, UserResponse, CurrentUserResponse
from utils.security import verify_password, create_access_token, get_password_hash
from datetime import datetime
from typing import Optional

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def login(db: Session, request: LoginRequest) -> LoginResponse:
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise ValueError("用户名或密码错误")
    
    user.last_login_at = datetime.now()
    db.commit()
    db.refresh(user)
    
    permissions = []
    if user.role:
        permissions = [p.code for p in user.role.permissions]
    
    access_token = create_access_token(data={"sub": user.id, "username": user.username})
    
    return LoginResponse(
        token=access_token,
        user=UserResponse(
            id=user.id,
            username=user.username,
            real_name=user.real_name,
            role=user.role.name if user.role else None,
            permissions=permissions
        )
    )

def get_current_user_info(user: User) -> CurrentUserResponse:
    permissions = []
    if user.role:
        permissions = [p.code for p in user.role.permissions]
    
    return CurrentUserResponse(
        id=user.id,
        username=user.username,
        real_name=user.real_name,
        department=user.department,
        role=user.role.name if user.role else None,
        permissions=permissions
    )
