from sqlalchemy.orm import Session
from models import Role, Permission, role_permissions
from schemas.role import RoleCreate, RoleUpdate, RoleResponse, RoleListResponse, PermissionResponse
from typing import Optional, List

def get_roles(db: Session, skip: int = 0, limit: int = 100) -> RoleListResponse:
    total = db.query(Role).count()
    roles = db.query(Role).offset(skip).limit(limit).all()
    
    role_responses = []
    for role in roles:
        permissions = [PermissionResponse(
            id=p.id,
            name=p.name,
            code=p.code,
            description=p.description,
            parent_id=p.parent_id,
            sort_order=p.sort_order
        ) for p in role.permissions]
        
        role_responses.append(RoleResponse(
            id=role.id,
            name=role.name,
            description=role.description,
            created_at=role.created_at,
            permissions=permissions
        ))
    
    return RoleListResponse(total=total, roles=role_responses)

def get_role_by_id(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.id == role_id).first()

def create_role(db: Session, role: RoleCreate) -> Role:
    db_role = Role(
        name=role.name,
        description=role.description
    )
    db.add(db_role)
    db.flush()
    
    if role.permission_ids:
        permissions = db.query(Permission).filter(Permission.id.in_(role.permission_ids)).all()
        db_role.permissions = permissions
    
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role_update: RoleUpdate) -> Optional[Role]:
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return None
    
    if role_update.name is not None:
        db_role.name = role_update.name
    if role_update.description is not None:
        db_role.description = role_update.description
    
    if role_update.permission_ids is not None:
        permissions = db.query(Permission).filter(Permission.id.in_(role_update.permission_ids)).all()
        db_role.permissions = permissions
    
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int) -> bool:
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return False
    
    db_role.permissions = []
    db.delete(db_role)
    db.commit()
    return True

def get_permissions(db: Session) -> List[PermissionResponse]:
    permissions = db.query(Permission).all()
    return [PermissionResponse(
        id=p.id,
        name=p.name,
        code=p.code,
        description=p.description,
        parent_id=p.parent_id,
        sort_order=p.sort_order
    ) for p in permissions]

def create_permission(db: Session, permission: dict) -> Permission:
    db_permission = Permission(**permission)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission
