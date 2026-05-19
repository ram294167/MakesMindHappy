"""Admin-only endpoints for dashboard data."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.models import Lead, Assessment, Booking, AssessmentResult
from app.schemas.schemas import AdminDashboardStats, LeadResponse, AssessmentResponse, BookingResponse
from typing import List

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats", response_model=AdminDashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get overview stats for the admin dashboard."""
    total_leads = db.query(func.count(Lead.id)).scalar() or 0
    new_leads = db.query(func.count(Lead.id)).filter(Lead.status == "new").scalar() or 0
    total_assessments = db.query(func.count(Assessment.id)).scalar() or 0
    completed_assessments = (
        db.query(func.count(Assessment.id))
        .filter(Assessment.status == "completed")
        .scalar() or 0
    )
    total_bookings = db.query(func.count(Booking.id)).scalar() or 0
    pending_bookings = (
        db.query(func.count(Booking.id))
        .filter(Booking.status == "pending")
        .scalar() or 0
    )
    return AdminDashboardStats(
        total_leads=total_leads,
        new_leads=new_leads,
        total_assessments=total_assessments,
        completed_assessments=completed_assessments,
        total_bookings=total_bookings,
        pending_bookings=pending_bookings,
    )


@router.get("/leads", response_model=List[LeadResponse])
def admin_get_leads(
    skip: int = 0,
    limit: int = 200,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all leads for admin."""
    query = db.query(Lead)
    if status:
        query = query.filter(Lead.status == status)
    return query.order_by(Lead.id.desc()).offset(skip).limit(limit).all()


@router.get("/assessments", response_model=List[AssessmentResponse])
def admin_get_assessments(
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db)
):
    """Get all assessments for admin."""
    return db.query(Assessment).order_by(
        Assessment.id.desc()
    ).offset(skip).limit(limit).all()


@router.get("/bookings", response_model=List[BookingResponse])
def admin_get_bookings(
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db)
):
    """Get all bookings for admin."""
    return db.query(Booking).order_by(
        Booking.id.desc()
    ).offset(skip).limit(limit).all()
