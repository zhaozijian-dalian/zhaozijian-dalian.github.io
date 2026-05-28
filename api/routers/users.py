from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserUpdate, UserListResponse
from services import get_users, get_user_by_id, create_user, update_user, delete_user
from middleware import get_current_user
from models import User

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.get("", response_model=UserListResponse)
def get_users_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_users(db, skip, limit)

@router.get("/{user_id}")
def get_user_route(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return user

@router.post("")
def create_user_route(user: UserCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{user_id}")
def update_user_route(user_id: int, user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return user

@router.delete("/{user_id}")
def delete_user_route(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return {"message": "删除成功"}
