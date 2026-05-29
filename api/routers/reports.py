from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas import ReportCreate, ReportUpdate, ReportListResponse, ReviewRequest, TimelineNode, DashboardStats
from services import (
    get_reports, get_report_by_id, create_report, update_report, delete_report,
    approve_report, reject_report, return_report, get_timeline, get_dashboard_stats
)
from middleware import get_current_user
from models import User
from typing import List, Optional

router = APIRouter(prefix="/infection-reports", tags=["院感报卡"])

@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_dashboard_stats(db)

@router.get("", response_model=ReportListResponse)
def get_reports_route(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_reports(db, skip, limit, status)

@router.get("/{report_id}")
def get_report_route(report_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="报卡不存在")
    return report

@router.post("")
def create_report_route(report: ReportCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return create_report(db, report, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{report_id}")
def update_report_route(report_id: int, report_update: ReportUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = update_report(db, report_id, report_update, current_user.id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="报卡不存在")
    return report

@router.delete("/{report_id}")
def delete_report_route(report_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    success = delete_report(db, report_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="报卡不存在")
    return {"message": "删除成功"}

@router.post("/{report_id}/approve")
def approve_report_route(report_id: int, review: ReviewRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = approve_report(db, report_id, current_user.id, review.comment)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="报卡不存在")
    return report

@router.post("/{report_id}/reject")
def reject_report_route(report_id: int, review: ReviewRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = reject_report(db, report_id, current_user.id, review.comment)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="报卡不存在")
    return report

@router.post("/{report_id}/return")
def return_report_route(report_id: int, review: ReviewRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = return_report(db, report_id, current_user.id, review.comment)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="报卡不存在")
    return report

@router.get("/{report_id}/timeline", response_model=List[TimelineNode])
def get_timeline_route(report_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    report = get_report_by_id(db, report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="报卡不存在")
    return get_timeline(db, report_id)
