from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    get_current_customer,
    get_current_officer,
    get_current_admin,
)
from app.services.loan_service import LoanService
from app.schemas.loan_schema import (
    LoanApplyRequest,
    LoanReviewRequest,
    LoanResponse,
    EMIResponse,
)

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/apply", response_model=LoanResponse, status_code=201)
def apply_loan(
    data: LoanApplyRequest,
    payload=Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return LoanService(db).apply(payload["sub"], data)


@router.get("", response_model=List[LoanResponse])
def list_loans(
    payload=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    svc = LoanService(db)
    if payload.get("role") in ["officer", "admin"]:
        return svc.get_all_loans()
    return svc.get_user_loans(payload["sub"])


@router.get("/{loan_id}/emi", response_model=EMIResponse)
def get_emi(
    loan_id: UUID,
    payload=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return LoanService(db).calculate_emi(loan_id)


@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(
    loan_id: UUID,
    payload=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = None if payload.get("role") in ["officer", "admin"] else payload["sub"]
    return LoanService(db).get_loan(loan_id, user_id)


@router.put("/{loan_id}/approve", response_model=LoanResponse)
def approve_loan(
    loan_id: UUID,
    data: LoanReviewRequest = LoanReviewRequest(),
    payload=Depends(get_current_officer),
    db: Session = Depends(get_db),
):
    return LoanService(db).approve(loan_id, payload["sub"], data)


@router.put("/{loan_id}/reject", response_model=LoanResponse)
def reject_loan(
    loan_id: UUID,
    data: LoanReviewRequest = LoanReviewRequest(),
    payload=Depends(get_current_officer),
    db: Session = Depends(get_db),
):
    return LoanService(db).reject(loan_id, payload["sub"], data)


@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(
    loan_id: UUID,
    data: LoanApplyRequest,
    payload=Depends(get_current_officer),
    db: Session = Depends(get_db),
):
    return LoanService(db).update_loan(
        loan_id,
        amount=data.amount,
        duration_months=data.duration_months,
        purpose=data.purpose,
    )


@router.delete("/{loan_id}", status_code=204)
def delete_loan(
    loan_id: UUID,
    payload=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    LoanService(db).delete_loan(loan_id)