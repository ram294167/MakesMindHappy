from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from urllib.parse import quote
from app.db.database import get_db
from app.models.models import Booking, Lead
from app.schemas.schemas import BookingCreate, BookingResponse, WhatsAppRedirectResponse
from app.core.config import settings
from typing import List

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

WHATSAPP_NUMBER = settings.WHATSAPP_NUMBER


@router.post("", response_model=BookingResponse, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    """Submit a session booking request and save as lead."""
    booking = Booking(
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        concern=payload.concern,
        session_type=payload.session_type or "student",
        preferred_time=payload.preferred_time,
        notes=payload.notes,
        status="pending",
    )
    db.add(booking)

    # Auto-create lead
    existing = db.query(Lead).filter(Lead.phone == payload.phone).first()
    if not existing:
        lead = Lead(
            name=payload.name,
            phone=payload.phone,
            email=payload.email,
            source="booking",
            status="new",
        )
        db.add(lead)

    db.commit()
    db.refresh(booking)
    return booking


@router.get("/whatsapp-redirect")
def get_whatsapp_redirect(
    name: str = "there",
    concern: str = "career guidance",
) -> WhatsAppRedirectResponse:
    """Generate a WhatsApp redirect URL with prefilled message."""
    message = (
        f"Hi, my name is {name}. I'd like to book a career guidance session. "
        f"My main concern: {concern}"
    )
    encoded = quote(message)
    url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"
    return WhatsAppRedirectResponse(
        url=url,
        phone=WHATSAPP_NUMBER,
        message=message,
    )


@router.get("", response_model=List[BookingResponse])
def list_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all bookings (admin use)."""
    return db.query(Booking).order_by(
        Booking.id.desc()
    ).offset(skip).limit(limit).all()


@router.patch("/{booking_id}/status")
def update_booking_status(
    booking_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update booking status."""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = status
    db.commit()
    return {"message": "Status updated", "booking_id": booking_id, "status": status}
