from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = 0

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    parent_id: Optional[int]
    sort_order: int
    
    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: List[int] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    permissions: List[PermissionResponse] = []
    
    class Config:
        from_attributes = True

class RoleListResponse(BaseModel):
    total: int
    roles: List[RoleResponse]
