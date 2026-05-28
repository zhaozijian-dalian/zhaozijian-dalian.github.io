from fastapi import FastAPI
from database import engine, Base
from middleware import setup_cors
from routers import auth_router, users_router, roles_router, reports_router
from config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="医院感染控制系统 API",
    description="医院感染控制系统的后端API服务",
    version="1.0.0"
)

setup_cors(app)

app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(users_router, prefix=settings.API_PREFIX)
app.include_router(roles_router, prefix=settings.API_PREFIX)
app.include_router(reports_router, prefix=settings.API_PREFIX)

@app.get("/")
def root():
    return {"message": "医院感染控制系统 API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
