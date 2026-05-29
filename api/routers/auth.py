from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import LoginRequest, LoginResponse, CurrentUserResponse
from services import login, get_current_user_info
from middleware import get_current_user
from models import User

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/login", response_model=LoginResponse)
def login_route(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        return login(db, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/logout")
def logout_route(current_user: User = Depends(get_current_user)):
    return {"message": "登出成功"}

@router.get("/current-user", response_model=CurrentUserResponse)
def get_current_user_route(current_user: User = Depends(get_current_user)):
    return get_current_user_info(current_user)
