from sqlalchemy import Column, Integer, String, DateTime, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class InfectionReport(Base):
    __tablename__ = "infection_reports"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_no = Column(String(50), unique=True, nullable=False, index=True)
    patient_name = Column(String(100), nullable=False)
    patient_id = Column(String(50), nullable=False)
    gender = Column(String(10))
    age = Column(Integer)
    department = Column(String(100))
    infection_type = Column(String(100))
    infection_date = Column(Date)
    diagnosis = Column(String(500))
    symptoms = Column(Text)
    treatment = Column(Text)
    status = Column(String(20), default="draft", index=True)
    reporter_id = Column(Integer, ForeignKey("users.id"))
    report_date = Column(Date)
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    review_date = Column(DateTime)
    review_comment = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    reporter = relationship("User", foreign_keys=[reporter_id], back_populates="reports")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviewed_reports")
    timeline_entries = relationship("Timeline", back_populates="report", order_by="Timeline.timestamp")

class Timeline(Base):
    __tablename__ = "timeline"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey("infection_reports.id"), nullable=False, index=True)
    action = Column(String(100), nullable=False)
    actor_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, server_default=func.now())
    comment = Column(Text)
    previous_status = Column(String(20))
    new_status = Column(String(20))
    
    report = relationship("InfectionReport", back_populates="timeline_entries")
    actor = relationship("User", back_populates="timeline_entries")

class OperationLog(Base):
    __tablename__ = "operation_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    timestamp = Column(DateTime, server_default=func.now())
    ip_address = Column(String(50))
    details = Column(Text)
    
    user = relationship("User", back_populates="operation_logs")
