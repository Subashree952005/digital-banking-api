from datetime import datetime, date
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.transaction import Transaction, TransactionType


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, tx_id: UUID) -> Transaction | None:
        return self.db.query(Transaction).filter(Transaction.id == tx_id).first()

    def get_by_account(self, account_id: UUID) -> list[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(
                (Transaction.from_account_id == account_id)
                | (Transaction.to_account_id == account_id)
            )
            .order_by(Transaction.created_at.desc())
            .all()
        )

    def create(
        self,
        amount: float,
        tx_type: TransactionType,
        from_account_id: UUID | None = None,
        to_account_id: UUID | None = None,
        description: str | None = None,
    ) -> Transaction:
        tx = Transaction(
            from_account_id=from_account_id,
            to_account_id=to_account_id,
            amount=amount,
            type=tx_type,
            description=description,
        )
        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def delete(self, tx: Transaction) -> None:
        self.db.delete(tx)
        self.db.commit()

    def count_today(self) -> int:
        today = date.today()
        return (
            self.db.query(Transaction)
            .filter(Transaction.created_at >= datetime(today.year, today.month, today.day))
            .count()
        )

    def get_all(self) -> list[Transaction]:
        return self.db.query(Transaction).order_by(Transaction.created_at.desc()).all()
