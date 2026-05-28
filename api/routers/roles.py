from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import RoleCreate, RoleUpdate, RoleListResponse, PermissionCreate, PermissionResponse
from services import get_roles, get_role_by_id, create_role, update_role, delete_role, get_permissions, create_permission
from middleware import get_current_user
from models import User
from typing import List

router = APIRouter(prefix="/roles", tags=["角色管理"])

@router.get("", response_model=RoleListResponse)
def get_roles_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_roles(db, skip, limit)

@router.get("/permissions", response_model=List[PermissionResponse])
def get_permissions_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_permissions(db)

@router.get("/{role_id}")
def get_role_route(role_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    role = get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
    return role

@router.post("")
def create_role_route(role: RoleCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return create_role(db, role)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{role_id}")
def update_role_route(role_id: int, role_update: RoleUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    role = update_role(db, role_id, role_update)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
    return role

@router.delete("/{role_id}")
def delete_role_route(role_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    success = delete_role(db, role_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="角色不存在")
    return {"message": "删除成功"}

@router.post("/permissions")
def create_permission_route(permission: PermissionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return create_permission(db, permission.model_dump())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
