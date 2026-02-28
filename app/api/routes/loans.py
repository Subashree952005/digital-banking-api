from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_customer, get_current_officer, get_current_admin, get_current_user
from app.services.loan_service import LoanService
from app.schemas.loan_schema import LoanApplyRequest, LoanReviewRequest, LoanResponse, EMIResponse

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/apply", response_model=LoanResponse, status_code=201)
def apply_loan(data: LoanApplyRequest, current_user=Depends(get_current_customer), db: Session = Depends(get_db)):
    return LoanService(db).apply(current_user.id, data)


@router.get("", response_model=List[LoanResponse])
def list_loans(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    from app.models.user import UserRole
    svc = LoanService(db)
    if current_user.role in [UserRole.officer, UserRole.admin]:
        return svc.get_all_loans()
    return svc.get_user_loans(current_user.id)


@router.get("/{loan_id}/emi", response_model=EMIResponse)
def get_emi(loan_id: UUID, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return LoanService(db).calculate_emi(loan_id)


@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: UUID, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    from app.models.user import UserRole
    user_id = None if current_user.role in [UserRole.officer, UserRole.admin] else current_user.id
    return LoanService(db).get_loan(loan_id, user_id)


@router.put("/{loan_id}/approve", response_model=LoanResponse)
def approve_loan(loan_id: UUID, data: LoanReviewRequest = LoanReviewRequest(), current_user=Depends(get_current_officer), db: Session = Depends(get_db)):
    return LoanService(db).approve(loan_id, current_user.id, data)


@router.put("/{loan_id}/reject", response_model=LoanResponse)
def reject_loan(loan_id: UUID, data: LoanReviewRequest = LoanReviewRequest(), current_user=Depends(get_current_officer), db: Session = Depends(get_db)):
    return LoanService(db).reject(loan_id, current_user.id, data)


@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(loan_id: UUID, data: LoanApplyRequest, current_user=Depends(get_current_officer), db: Session = Depends(get_db)):
    return LoanService(db).update_loan(loan_id, amount=data.amount, duration_months=data.duration_months, purpose=data.purpose)


@router.delete("/{loan_id}", status_code=204)
def delete_loan(loan_id: UUID, current_user=Depends(get_current_admin), db: Session = Depends(get_db)):
    LoanService(db).delete_loan(loan_id)
