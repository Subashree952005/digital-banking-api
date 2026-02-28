from sqlalchemy.orm import Session
from app.models.loan import Loan, LoanStatus


class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, loan_id) -> Loan | None:
        return self.db.query(Loan).filter(Loan.id == loan_id).first()

    def get_by_user(self, user_id) -> list[Loan]:
        return self.db.query(Loan).filter(Loan.user_id == user_id).all()

    def get_all(self) -> list[Loan]:
        return self.db.query(Loan).all()

    def create(self, user_id, amount: float, duration_months: int, purpose: str | None = None) -> Loan:
        loan = Loan(
            user_id=user_id,
            amount=amount,
            duration_months=duration_months,
            purpose=purpose,
        )
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def update(self, loan: Loan, **kwargs) -> Loan:
        for k, v in kwargs.items():
            setattr(loan, k, v)
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def delete(self, loan: Loan) -> None:
        self.db.delete(loan)
        self.db.commit()

    def count_all(self) -> int:
        return self.db.query(Loan).count()

    def count_pending(self) -> int:
        return self.db.query(Loan).filter(Loan.status == LoanStatus.pending).count()