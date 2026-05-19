"""Public read endpoints for careers, pricing, testimonials, FAQs."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import CareerOption, PricingPlan, Testimonial, FAQ
from app.schemas.schemas import (
    PricingPlanResponse, TestimonialResponse, FAQResponse
)
from typing import List

router = APIRouter(prefix="/api", tags=["Public"])


@router.get("/careers")
def list_careers(db: Session = Depends(get_db)):
    """List all active career options."""
    careers = db.query(CareerOption).filter(
        CareerOption.is_active == True
    ).all()
    return careers


@router.get("/pricing", response_model=List[PricingPlanResponse])
def list_pricing(db: Session = Depends(get_db)):
    """List all active pricing plans."""
    return db.query(PricingPlan).filter(
        PricingPlan.is_active == True
    ).order_by(PricingPlan.order_index).all()


@router.get("/testimonials", response_model=List[TestimonialResponse])
def list_testimonials(db: Session = Depends(get_db)):
    """List active testimonials."""
    return db.query(Testimonial).filter(
        Testimonial.is_active == True
    ).all()


@router.get("/faq", response_model=List[FAQResponse])
def list_faqs(db: Session = Depends(get_db)):
    """List all active FAQs."""
    return db.query(FAQ).filter(
        FAQ.is_active == True
    ).order_by(FAQ.order_index).all()
