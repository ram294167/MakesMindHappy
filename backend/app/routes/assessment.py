from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Assessment, AssessmentResult, Lead
from app.schemas.schemas import (
    AssessmentStartRequest, AssessmentAnswerRequest,
    AssessmentResponse, ResultResponse
)
from app.services.career_service import generate_result
from typing import List

router = APIRouter(prefix="/api/assessment", tags=["Assessment"])


def _save_lead_from_assessment(db: Session, info):
    """Automatically create a lead when assessment is started."""
    if info.phone:
        existing = db.query(Lead).filter(Lead.phone == info.phone).first()
        if not existing:
            lead = Lead(
                name=info.name,
                phone=info.phone,
                email=info.email,
                city=info.city,
                source="assessment",
                status="new",
            )
            db.add(lead)
            db.commit()


@router.post("/start", response_model=AssessmentResponse, status_code=201)
def start_assessment(
    payload: AssessmentStartRequest,
    db: Session = Depends(get_db)
):
    """Start a new assessment and optionally save answers in one call."""
    info = payload.personalInfo

    # Create assessment record
    assessment = Assessment(
        student_name=info.name,
        age=int(info.age) if info.age and info.age.isdigit() else None,
        class_year=info.classYear,
        school=info.school,
        city=info.city,
        phone=info.phone,
        email=info.email,
        main_confusion=info.mainConfusion,
        status="started",
    )

    # If answers were also submitted (single-shot submission)
    if payload.answers:
        assessment.answers = payload.answers
        assessment.status = "completed"

        # Generate result immediately
        result_data = generate_result(0, payload.answers)
        db.add(assessment)
        db.flush()  # get the assessment.id

        result = AssessmentResult(
            assessment_id=assessment.id,
            **{k: v for k, v in result_data.items() if k != "assessment_id"}
        )
        db.add(result)
    else:
        db.add(assessment)

    db.commit()
    db.refresh(assessment)

    # Save a lead record
    _save_lead_from_assessment(db, info)

    return assessment


@router.post("/answer")
def submit_answers(
    payload: AssessmentAnswerRequest,
    db: Session = Depends(get_db)
):
    """Submit answers to an existing assessment."""
    assessment = db.query(Assessment).filter(
        Assessment.id == payload.assessment_id
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment.answers = payload.answers
    assessment.status = "completed"

    # Generate result
    result_data = generate_result(assessment.id, payload.answers)
    result = AssessmentResult(
        assessment_id=assessment.id,
        **{k: v for k, v in result_data.items() if k != "assessment_id"}
    )
    db.add(result)
    db.commit()
    db.refresh(assessment)

    return {"message": "Answers submitted", "assessment_id": assessment.id}


@router.get("/result/{assessment_id}", response_model=ResultResponse)
def get_result(assessment_id: int, db: Session = Depends(get_db)):
    """Get result for a completed assessment."""
    result = db.query(AssessmentResult).filter(
        AssessmentResult.assessment_id == assessment_id
    ).first()
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Result not found. Assessment may still be processing."
        )
    return result


@router.get("/list", response_model=List[AssessmentResponse])
def list_assessments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all assessments (admin use)."""
    return db.query(Assessment).order_by(
        Assessment.id.desc()
    ).offset(skip).limit(limit).all()
