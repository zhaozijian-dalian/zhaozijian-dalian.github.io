from fastapi import FastAPI
from database import engine, Base, SessionLocal
from middleware import setup_cors
from routers import auth, users, roles, reports
from config import settings
from models import User, Role, Permission
from utils import security

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="医院感染控制系统 API",
    description="医院感染控制系统的后端API服务",
    version="1.0.0"
)

setup_cors(app)

app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(users.router, prefix=settings.API_PREFIX)
app.include_router(roles.router, prefix=settings.API_PREFIX)
app.include_router(reports.router, prefix=settings.API_PREFIX)

def init_db():
    db = SessionLocal()
    try:
        if not db.query(Role).first():
            role_admin = Role(name="系统管理员", description="系统管理员，拥有所有权限")
            role_supervisor = Role(name="院感科主任", description="院感科主任，负责审核报卡")
            role_staff = Role(name="院感专职人员", description="院感专职人员，负责报卡管理")
            role_doctor = Role(name="临床医生", description="临床医生，负责本科室报卡")
            role_nurse = Role(name="护士长", description="护士长，负责本科室报卡审核")
            
            db.add_all([role_admin, role_supervisor, role_staff, role_doctor, role_nurse])
            db.commit()
            
            perm1 = Permission(name="系统管理", code="system", description="系统管理模块", parent_id=None, sort_order=1)
            perm2 = Permission(name="用户管理", code="user:management", description="用户管理", parent_id=1, sort_order=1)
            perm3 = Permission(name="用户列表", code="user:list", description="查看用户列表", parent_id=2, sort_order=1)
            perm4 = Permission(name="用户新增", code="user:create", description="新增用户", parent_id=2, sort_order=2)
            perm5 = Permission(name="用户编辑", code="user:edit", description="编辑用户", parent_id=2, sort_order=3)
            perm6 = Permission(name="用户删除", code="user:delete", description="删除用户", parent_id=2, sort_order=4)
            perm7 = Permission(name="权限管理", code="role:management", description="权限管理", parent_id=1, sort_order=2)
            perm8 = Permission(name="角色列表", code="role:list", description="查看角色列表", parent_id=7, sort_order=1)
            perm9 = Permission(name="角色新增", code="role:create", description="新增角色", parent_id=7, sort_order=2)
            perm10 = Permission(name="角色编辑", code="role:edit", description="编辑角色", parent_id=7, sort_order=3)
            perm11 = Permission(name="角色删除", code="role:delete", description="删除角色", parent_id=7, sort_order=4)
            perm12 = Permission(name="院感管理", code="report:management", description="院感报卡管理", parent_id=None, sort_order=2)
            perm13 = Permission(name="报卡列表", code="report:list", description="查看报卡列表", parent_id=12, sort_order=1)
            perm14 = Permission(name="报卡录入", code="report:create", description="录入报卡", parent_id=12, sort_order=2)
            perm15 = Permission(name="报卡编辑", code="report:edit", description="编辑报卡", parent_id=12, sort_order=3)
            perm16 = Permission(name="报卡删除", code="report:delete", description="删除报卡", parent_id=12, sort_order=4)
            perm17 = Permission(name="报卡审核", code="report:review", description="审核报卡", parent_id=12, sort_order=5)
            perm18 = Permission(name="报卡退回", code="report:return", description="退回报卡", parent_id=12, sort_order=6)
            perm19 = Permission(name="仪表盘", code="dashboard:view", description="查看仪表盘", parent_id=None, sort_order=3)
            
            db.add_all([perm1, perm2, perm3, perm4, perm5, perm6, perm7, perm8, perm9, perm10, 
                       perm11, perm12, perm13, perm14, perm15, perm16, perm17, perm18, perm19])
            db.commit()
            
            role_admin.permissions = [perm1, perm2, perm3, perm4, perm5, perm6, perm7, perm8, perm9, 
                                     perm10, perm11, perm12, perm13, perm14, perm15, perm16, perm17, perm18, perm19]
            role_supervisor.permissions = [perm13, perm17, perm18, perm19]
            role_staff.permissions = [perm13, perm14, perm15, perm16, perm19]
            role_doctor.permissions = [perm13, perm14, perm19]
            role_nurse.permissions = [perm13, perm17, perm18, perm19]
            
            db.commit()
            
            hashed_password = security.get_password_hash("admin123")
            admin_user = User(
                username="admin",
                password_hash=hashed_password,
                real_name="系统管理员",
                department="信息中心",
                role_id=role_admin.id,
                status="active"
            )
            db.add(admin_user)
            db.commit()
            print("Database initialized with seed data!")
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()

init_db()

@app.get("/")
def root():
    return {"message": "医院感染控制系统 API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
