from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.loan_repository import LoanRepository
from app.models.loan import LoanStatus
from app.schemas.loan_schema import LoanApplyRequest, LoanReviewRequest, EMIResponse


class LoanService:
    def __init__(self, db: Session):
        self.repo = LoanRepository(db)

    def apply(self, user_id, data: LoanApplyRequest):
        if data.amount <= 0:
            raise HTTPException(status_code=400, detail="Loan amount must be positive")
        if data.duration_months < 1:
            raise HTTPException(status_code=400, detail="Duration must be at least 1 month")
        return self.repo.create(
            user_id=user_id,
            amount=data.amount,
            duration_months=data.duration_months,
            purpose=data.purpose,
        )

    def get_loan(self, loan_id, user_id=None):
        loan = self.repo.get_by_id(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        if user_id and str(loan.user_id) != str(user_id):
            raise HTTPException(status_code=403, detail="Not your loan")
        return loan

    def get_user_loans(self, user_id):
        return self.repo.get_by_user(user_id)

    def get_all_loans(self):
        return self.repo.get_all()

    def approve(self, loan_id, officer_id, data: LoanReviewRequest):
        loan = self.repo.get_by_id(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        if loan.status != LoanStatus.pending:
            raise HTTPException(status_code=400, detail="Loan is not pending")
        return self.repo.update(
            loan,
            status=LoanStatus.approved,
            officer_id=officer_id,
            officer_note=data.officer_note,
            reviewed_at=datetime.utcnow(),
        )

    def reject(self, loan_id, officer_id, data: LoanReviewRequest):
        loan = self.repo.get_by_id(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        if loan.status != LoanStatus.pending:
            raise HTTPException(status_code=400, detail="Loan is not pending")
        return self.repo.update(
            loan,
            status=LoanStatus.rejected,
            officer_id=officer_id,
            officer_note=data.officer_note,
            reviewed_at=datetime.utcnow(),
        )

    def update_loan(self, loan_id, **kwargs):
        loan = self.repo.get_by_id(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        return self.repo.update(loan, **kwargs)

    def delete_loan(self, loan_id):
        loan = self.repo.get_by_id(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        self.repo.delete(loan)

    def calculate_emi(self, loan_id) -> EMIResponse:
        loan = self.repo.get_by_id(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        r = loan.interest_rate / 100 / 12
        n = int(loan.duration_months)
        if r == 0:
            emi = loan.amount / n
        else:
            emi = loan.amount * r * (1 + r) ** n / ((1 + r) ** n - 1)
        total = emi * n
        return EMIResponse(
            loan_id=loan.id,
            principal=loan.amount,
            interest_rate=loan.interest_rate,
            duration_months=loan.duration_months,
            monthly_emi=round(emi, 2),
            total_payable=round(total, 2),
            total_interest=round(total - loan.amount, 2),
        )