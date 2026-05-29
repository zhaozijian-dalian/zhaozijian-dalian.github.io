from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ReportBase(BaseModel):
    patient_name: str
    patient_id: str
    gender: Optional[str] = None
    age: Optional[int] = None
    department: Optional[str] = None
    infection_type: Optional[str] = None
    infection_date: Optional[date] = None
    diagnosis: Optional[str] = None
    symptoms: Optional[str] = None
    treatment: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    patient_name: Optional[str] = None
    patient_id: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    department: Optional[str] = None
    infection_type: Optional[str] = None
    infection_date: Optional[date] = None
    diagnosis: Optional[str] = None
    symptoms: Optional[str] = None
    treatment: Optional[str] = None

class ReportResponse(BaseModel):
    id: int
    report_no: str
    patient_name: str
    patient_id: str
    gender: Optional[str]
    age: Optional[int]
    department: Optional[str]
    infection_type: Optional[str]
    infection_date: Optional[date]
    diagnosis: Optional[str]
    symptoms: Optional[str]
    treatment: Optional[str]
    status: str
    reporter: Optional[str]
    report_date: Optional[date]
    reviewer: Optional[str]
    review_date: Optional[datetime]
    review_comment: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ReportListResponse(BaseModel):
    total: int
    reports: list[ReportResponse]

class TimelineNode(BaseModel):
    id: int
    report_id: int
    action: str
    actor: Optional[str]
    timestamp: datetime
    comment: Optional[str]
    previous_status: Optional[str]
    new_status: Optional[str]
    
    class Config:
        from_attributes = True

class ReviewRequest(BaseModel):
    comment: Optional[str] = None

class DashboardStats(BaseModel):
    today_reports: int
    pending_reviews: int
    monthly_total: int
    approved_rate: float
    weekly_trend: list[dict]
    infection_type_distribution: list[dict]
