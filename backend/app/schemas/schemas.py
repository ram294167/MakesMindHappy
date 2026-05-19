from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any, Dict
from datetime import datetime


# ── Lead ────────────────────────────────────────────────────────────────────

class LeadCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    city: Optional[str] = None
    source: Optional[str] = "direct"
    notes: Optional[str] = None
    message: Optional[str] = None  # contact form message


class LeadResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    city: Optional[str]
    source: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LeadStatusUpdate(BaseModel):
    status: str


# ── Assessment ───────────────────────────────────────────────────────────────

class PersonalInfo(BaseModel):
    name: str
    age: Optional[str] = None
    classYear: Optional[str] = None
    school: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    mainConfusion: Optional[str] = None


class AssessmentStartRequest(BaseModel):
    personalInfo: PersonalInfo
    answers: Optional[Dict[str, str]] = None


class AssessmentAnswerRequest(BaseModel):
    assessment_id: int
    answers: Dict[str, str]


class AssessmentResponse(BaseModel):
    id: int
    student_name: str
    class_year: Optional[str]
    city: Optional[str]
    phone: str
    email: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Result ───────────────────────────────────────────────────────────────────

class ResultResponse(BaseModel):
    id: int
    assessment_id: int
    overall_score: Optional[float]
    aptitude_score: Optional[float]
    personality_score: Optional[float]
    eq_score: Optional[float]
    learning_style: Optional[str]
    interest_score: Optional[float]
    career_fit_score: Optional[float]
    top_careers: Optional[List[Any]]
    stream_recommendation: Optional[Dict]
    strengths: Optional[List[str]]
    skill_gaps: Optional[List[str]]
    action_plan: Optional[List[str]]
    mentor_notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ── Booking ──────────────────────────────────────────────────────────────────

class BookingCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    concern: Optional[str] = None
    session_type: Optional[str] = "student"
    preferred_time: Optional[str] = None
    notes: Optional[str] = None


class BookingResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    concern: Optional[str]
    session_type: str
    preferred_time: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── WhatsApp ─────────────────────────────────────────────────────────────────

class WhatsAppRedirectResponse(BaseModel):
    url: str
    phone: str
    message: str


# ── Testimonial ──────────────────────────────────────────────────────────────

class TestimonialResponse(BaseModel):
    id: int
    name: str
    role: Optional[str]
    text: str
    stars: int
    emoji: Optional[str]

    class Config:
        from_attributes = True


# ── FAQ ──────────────────────────────────────────────────────────────────────

class FAQResponse(BaseModel):
    id: int
    category: str
    question: str
    answer: str
    order_index: int

    class Config:
        from_attributes = True


# ── Pricing ──────────────────────────────────────────────────────────────────

class PricingPlanResponse(BaseModel):
    id: int
    name: str
    emoji: Optional[str]
    price: str
    original_price: Optional[str]
    tagline: Optional[str]
    description: Optional[str]
    includes: Optional[List[str]]
    suitable_for: Optional[str]
    is_highlighted: bool
    badge: Optional[str]

    class Config:
        from_attributes = True


# ── Admin ────────────────────────────────────────────────────────────────────

class AdminDashboardStats(BaseModel):
    total_leads: int
    new_leads: int
    total_assessments: int
    completed_assessments: int
    total_bookings: int
    pending_bookings: int
