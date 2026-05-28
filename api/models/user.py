from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    real_name = Column(String(100), nullable=False)
    department = Column(String(100))
    role_id = Column(Integer, ForeignKey("roles.id"))
    status = Column(String(20), default="active")
    created_at = Column(DateTime, server_default=func.now())
    last_login_at = Column(DateTime)
    
    role = relationship("Role", back_populates="users")
    reports = relationship("InfectionReport", foreign_keys="InfectionReport.reporter_id", back_populates="reporter")
    reviewed_reports = relationship("InfectionReport", foreign_keys="InfectionReport.reviewer_id", back_populates="reviewer")
    timeline_entries = relationship("Timeline", back_populates="actor")
    operation_logs = relationship("OperationLog", back_populates="user")
