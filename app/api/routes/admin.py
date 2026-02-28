from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sqlalchemy
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.loan_repository import LoanRepository

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/reports")
def get_reports(current_user=Depends(get_current_admin), db: Session = Depends(get_db)):
    acc_repo = AccountRepository(db)
    tx_repo = TransactionRepository(db)
    loan_repo = LoanRepository(db)
    accounts = acc_repo.get_all()
    total_balance = sum(a.balance for a in accounts)
    total_users = db.execute(sqlalchemy.text("SELECT COUNT(*) FROM users")).scalar()
    return {
        "total_users": total_users,
        "total_accounts": len(accounts),
        "total_loans": loan_repo.count_all(),
        "pending_loans": loan_repo.count_pending(),
        "total_transactions_today": tx_repo.count_today(),
        "total_balance_in_system": round(total_balance, 2),
    }