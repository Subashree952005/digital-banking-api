from sqlalchemy.orm import Session
from app.models.account import Account, AccountStatus


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, account_id) -> Account | None:
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_by_number(self, account_number: str) -> Account | None:
        return self.db.query(Account).filter(Account.account_number == account_number).first()

    def get_by_user(self, user_id) -> list[Account]:
        return self.db.query(Account).filter(Account.user_id == user_id).all()

    def update(self, account: Account, **kwargs) -> Account:
        for k, v in kwargs.items():
            setattr(account, k, v)
        self.db.commit()
        self.db.refresh(account)
        return account