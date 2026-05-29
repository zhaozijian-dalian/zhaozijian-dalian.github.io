from sqlalchemy.orm import Session
from models import InfectionReport, Timeline, User
from schemas.report import ReportCreate, ReportUpdate, ReportResponse, ReportListResponse, TimelineNode, ReviewRequest, DashboardStats
from datetime import date, datetime, timedelta
from typing import Optional
import random
import string

def generate_report_no() -> str:
    date_str = date.today().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.digits, k=4))
    return f"HIC-{date_str}-{random_str}"

def get_reports(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> ReportListResponse:
    query = db.query(InfectionReport)
    
    if status:
        query = query.filter(InfectionReport.status == status)
    
    total = query.count()
    reports = query.order_by(InfectionReport.created_at.desc()).offset(skip).limit(limit).all()
    
    report_responses = []
    for report in reports:
        report_responses.append(ReportResponse(
            id=report.id,
            report_no=report.report_no,
            patient_name=report.patient_name,
            patient_id=report.patient_id,
            gender=report.gender,
            age=report.age,
            department=report.department,
            infection_type=report.infection_type,
            infection_date=report.infection_date,
            diagnosis=report.diagnosis,
            symptoms=report.symptoms,
            treatment=report.treatment,
            status=report.status,
            reporter=report.reporter.real_name if report.reporter else None,
            report_date=report.report_date,
            reviewer=report.reviewer.real_name if report.reviewer else None,
            review_date=report.review_date,
            review_comment=report.review_comment,
            created_at=report.created_at,
            updated_at=report.updated_at
        ))
    
    return ReportListResponse(total=total, reports=report_responses)

def get_report_by_id(db: Session, report_id: int) -> Optional[InfectionReport]:
    return db.query(InfectionReport).filter(InfectionReport.id == report_id).first()

def create_report(db: Session, report: ReportCreate, user_id: int) -> InfectionReport:
    db_report = InfectionReport(
        report_no=generate_report_no(),
        patient_name=report.patient_name,
        patient_id=report.patient_id,
        gender=report.gender,
        age=report.age,
        department=report.department,
        infection_type=report.infection_type,
        infection_date=report.infection_date,
        diagnosis=report.diagnosis,
        symptoms=report.symptoms,
        treatment=report.treatment,
        status="pending",
        reporter_id=user_id,
        report_date=date.today()
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    timeline = Timeline(
        report_id=db_report.id,
        action="创建报卡",
        actor_id=user_id,
        new_status="pending",
        comment="首次提交"
    )
    db.add(timeline)
    db.commit()
    
    return db_report

def update_report(db: Session, report_id: int, report_update: ReportUpdate, user_id: int) -> Optional[InfectionReport]:
    db_report = db.query(InfectionReport).filter(InfectionReport.id == report_id).first()
    if not db_report:
        return None
    
    update_data = report_update.model_dump(exclude_unset=True)
    previous_status = db_report.status
    
    for field, value in update_data.items():
        setattr(db_report, field, value)
    
    db_report.updated_at = datetime.now()
    
    if previous_status == "returned" and update_data:
        db_report.status = "pending"
        timeline = Timeline(
            report_id=db_report.id,
            action="重新提交",
            actor_id=user_id,
            previous_status="returned",
            new_status="pending",
            comment="修改后重新提交"
        )
        db.add(timeline)
    
    db.commit()
    db.refresh(db_report)
    return db_report

def delete_report(db: Session, report_id: int) -> bool:
    db_report = db.query(InfectionReport).filter(InfectionReport.id == report_id).first()
    if not db_report:
        return False
    
    db.query(Timeline).filter(Timeline.report_id == report_id).delete()
    db.delete(db_report)
    db.commit()
    return True

def approve_report(db: Session, report_id: int, user_id: int, comment: Optional[str] = None) -> Optional[InfectionReport]:
    db_report = db.query(InfectionReport).filter(InfectionReport.id == report_id).first()
    if not db_report:
        return None
    
    previous_status = db_report.status
    db_report.status = "approved"
    db_report.reviewer_id = user_id
    db_report.review_date = datetime.now()
    db_report.review_comment = comment
    
    timeline = Timeline(
        report_id=db_report.id,
        action="审核通过",
        actor_id=user_id,
        previous_status=previous_status,
        new_status="approved",
        comment=comment
    )
    db.add(timeline)
    db.commit()
    db.refresh(db_report)
    return db_report

def reject_report(db: Session, report_id: int, user_id: int, comment: Optional[str] = None) -> Optional[InfectionReport]:
    db_report = db.query(InfectionReport).filter(InfectionReport.id == report_id).first()
    if not db_report:
        return None
    
    previous_status = db_report.status
    db_report.status = "rejected"
    db_report.reviewer_id = user_id
    db_report.review_date = datetime.now()
    db_report.review_comment = comment
    
    timeline = Timeline(
        report_id=db_report.id,
        action="审核驳回",
        actor_id=user_id,
        previous_status=previous_status,
        new_status="rejected",
        comment=comment
    )
    db.add(timeline)
    db.commit()
    db.refresh(db_report)
    return db_report

def return_report(db: Session, report_id: int, user_id: int, comment: Optional[str] = None) -> Optional[InfectionReport]:
    db_report = db.query(InfectionReport).filter(InfectionReport.id == report_id).first()
    if not db_report:
        return None
    
    previous_status = db_report.status
    db_report.status = "returned"
    db_report.reviewer_id = user_id
    db_report.review_date = datetime.now()
    db_report.review_comment = comment
    
    timeline = Timeline(
        report_id=db_report.id,
        action="退回修改",
        actor_id=user_id,
        previous_status=previous_status,
        new_status="returned",
        comment=comment
    )
    db.add(timeline)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_timeline(db: Session, report_id: int) -> list[TimelineNode]:
    timeline_entries = db.query(Timeline).filter(Timeline.report_id == report_id).order_by(Timeline.timestamp.asc()).all()
    
    nodes = []
    for entry in timeline_entries:
        nodes.append(TimelineNode(
            id=entry.id,
            report_id=entry.report_id,
            action=entry.action,
            actor=entry.actor.real_name if entry.actor else None,
            timestamp=entry.timestamp,
            comment=entry.comment,
            previous_status=entry.previous_status,
            new_status=entry.new_status
        ))
    
    return nodes

def get_dashboard_stats(db: Session) -> DashboardStats:
    today = date.today()
    month_start = today.replace(day=1)
    
    today_reports = db.query(InfectionReport).filter(
        InfectionReport.report_date == today
    ).count()
    
    pending_reviews = db.query(InfectionReport).filter(
        InfectionReport.status == "pending"
    ).count()
    
    monthly_total = db.query(InfectionReport).filter(
        InfectionReport.report_date >= month_start
    ).count()
    
    approved_count = db.query(InfectionReport).filter(
        InfectionReport.status == "approved"
    ).count()
    total_count = db.query(InfectionReport).count()
    approved_rate = (approved_count / total_count * 100) if total_count > 0 else 0.0
    
    weekly_trend = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = db.query(InfectionReport).filter(
            InfectionReport.report_date == day
        ).count()
        weekly_trend.append({"date": day.strftime("%m-%d"), "count": count})
    
    infection_types = db.query(InfectionReport.infection_type, db.func.count(InfectionReport.id)).group_by(InfectionReport.infection_type).all()
    infection_type_distribution = [
        {"type": it[0] or "未知", "count": it[1]} for it in infection_types
    ]
    
    return DashboardStats(
        today_reports=today_reports,
        pending_reviews=pending_reviews,
        monthly_total=monthly_total,
        approved_rate=round(approved_rate, 2),
        weekly_trend=weekly_trend,
        infection_type_distribution=infection_type_distribution
    )
