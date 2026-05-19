from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Lead
from app.schemas.schemas import LeadCreate, LeadResponse, LeadStatusUpdate
from typing import List

router = APIRouter(prefix="/api/leads", tags=["Leads"])


@router.post("", response_model=LeadResponse, status_code=201)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    """Capture a new lead from any form on the site."""
    lead = Lead(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        city=payload.city,
        source=payload.source or "direct",
        notes=payload.message or payload.notes,
        status="new",
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("", response_model=List[LeadResponse])
def list_leads(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db)
):
    """List all leads (admin use)."""
    query = db.query(Lead)
    if status:
        query = query.filter(Lead.status == status)
    return query.order_by(Lead.id.desc()).offset(skip).limit(limit).all()


@router.patch("/{lead_id}/status", response_model=LeadResponse)
def update_lead_status(
    lead_id: int,
    payload: LeadStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update a lead's follow-up status."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = payload.status
    db.commit()
    db.refresh(lead)
    return lead
