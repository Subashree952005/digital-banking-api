import random
import string
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.account import Account, AccountStatus


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def generate_account_number(self) -> str:
        while True:
            number = "".join(random.choices(string.digits, k=10))
            if not self.db.query(Account).filter(Account.account_number == number).first():
                return number

    def get_by_id(self, account_id: UUID) -> Account | None:
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_by_number(self, account_number: str) -> Account | None:
        return self.db.query(Account).filter(Account.account_number == account_number).first()

    def get_by_user(self, user_id: UUID) -> list[Account]:
        return self.db.query(Account).filter(Account.user_id == user_id).all()

    def create(self, user_id: UUID, initial_deposit: float = 0.0) -> Account:
        account = Account(
            user_id=user_id,
            account_number=self.generate_account_number(),
            balance=initial_deposit,
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update(self, account: Account, **kwargs) -> Account:
        for k, v in kwargs.items():
            setattr(account, k, v)
        self.db.commit()
        self.db.refresh(account)
        return account

    def delete(self, account: Account) -> None:
        self.db.delete(account)
        self.db.commit()

    def get_all(self) -> list[Account]:
        return self.db.query(Account).all()
