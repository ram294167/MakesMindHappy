from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean,
    DateTime, ForeignKey, JSON, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class LeadSource(str, enum.Enum):
    assessment = "assessment"
    contact_form = "contact_form"
    booking = "booking"
    whatsapp = "whatsapp"
    direct = "direct"


class LeadStatus(str, enum.Enum):
    new = "new"
    contacted = "contacted"
    in_progress = "in_progress"
    completed = "completed"
    lost = "lost"


class AssessmentStatus(str, enum.Enum):
    started = "started"
    in_progress = "in_progress"
    completed = "completed"
    reviewed = "reviewed"


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    source = Column(String(50), default="direct")
    status = Column(String(50), default="new")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(200), nullable=False)
    age = Column(Integer, nullable=True)
    class_year = Column(String(50), nullable=True)
    school = Column(String(300), nullable=True)
    city = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    main_confusion = Column(String(200), nullable=True)
    goal = Column(String(200), nullable=True)
    status = Column(String(50), default="started")
    answers = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to result
    result = relationship("AssessmentResult", back_populates="assessment", uselist=False)


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)

    # Scores
    overall_score = Column(Float, nullable=True)
    aptitude_score = Column(Float, nullable=True)
    personality_score = Column(Float, nullable=True)
    eq_score = Column(Float, nullable=True)
    learning_style = Column(String(100), nullable=True)
    interest_score = Column(Float, nullable=True)
    career_fit_score = Column(Float, nullable=True)

    # Results
    top_careers = Column(JSON, nullable=True)       # list of career objects
    stream_recommendation = Column(JSON, nullable=True)
    strengths = Column(JSON, nullable=True)         # list of strings
    skill_gaps = Column(JSON, nullable=True)        # list of strings
    action_plan = Column(JSON, nullable=True)       # list of steps
    mentor_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to assessment
    assessment = relationship("Assessment", back_populates="result")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    concern = Column(String(300), nullable=True)
    session_type = Column(String(50), default="student")
    preferred_time = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    role = Column(String(200), nullable=True)
    text = Column(Text, nullable=False)
    stars = Column(Integer, default=5)
    emoji = Column(String(10), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CareerOption(Base):
    __tablename__ = "career_options"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    emoji = Column(String(10), nullable=True)
    description = Column(Text, nullable=True)
    suitable_streams = Column(JSON, nullable=True)
    required_strengths = Column(JSON, nullable=True)
    aptitude_range = Column(JSON, nullable=True)  # {"min": 60, "max": 100}
    personality_types = Column(JSON, nullable=True)
    interest_areas = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)


class PricingPlan(Base):
    __tablename__ = "pricing_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    emoji = Column(String(10), nullable=True)
    price = Column(String(50), nullable=False)
    original_price = Column(String(50), nullable=True)
    tagline = Column(String(300), nullable=True)
    description = Column(Text, nullable=True)
    includes = Column(JSON, nullable=True)  # list of strings
    suitable_for = Column(String(300), nullable=True)
    is_highlighted = Column(Boolean, default=False)
    badge = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    order_index = Column(Integer, default=0)
