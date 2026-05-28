from sqlalchemy.orm import Session
from models import User
from schemas.user import UserCreate, UserUpdate, UserResponse as UserResponseSchema, UserListResponse
from utils.security import get_password_hash
from typing import Optional, List

def get_users(db: Session, skip: int = 0, limit: int = 100) -> UserListResponse:
    total = db.query(User).count()
    users = db.query(User).offset(skip).limit(limit).all()
    
    user_responses = []
    for user in users:
        user_responses.append(UserResponseSchema(
            id=user.id,
            username=user.username,
            real_name=user.real_name,
            department=user.department,
            role=user.role.name if user.role else None,
            status=user.status,
            created_at=user.created_at,
            last_login_at=user.last_login_at
        ))
    
    return UserListResponse(total=total, users=user_responses)

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        password_hash=hashed_password,
        real_name=user.real_name,
        department=user.department,
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True
