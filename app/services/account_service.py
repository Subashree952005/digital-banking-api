from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.repositories.account_repository import AccountRepository
from app.models.account import AccountStatus
from app.schemas.account_schema import CreateAccountRequest, AccountUpdateRequest


class AccountService:
    def __init__(self, db: Session):
        self.repo = AccountRepository(db)

    def create_account(self, user_id: UUID, data: CreateAccountRequest):
        if data.initial_deposit < 0:
            raise HTTPException(status_code=400, detail="Initial deposit cannot be negative")
        return self.repo.create(user_id=user_id, initial_deposit=data.initial_deposit)

    def get_account(self, account_id: UUID, user_id: UUID | None = None):
        account = self.repo.get_by_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if user_id and account.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not your account")
        return account

    def get_user_accounts(self, user_id: UUID):
        return self.repo.get_by_user(user_id)

    def update_account(self, account_id: UUID, user_id: UUID, data: AccountUpdateRequest):
        account = self.get_account(account_id, user_id)
        updates = data.model_dump(exclude_none=True)
        return self.repo.update(account, **updates)

    def freeze_account(self, account_id: UUID):
        account = self.repo.get_by_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return self.repo.update(account, status=AccountStatus.frozen)

    def close_account(self, account_id: UUID):
        account = self.repo.get_by_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if account.balance > 0:
            raise HTTPException(status_code=400, detail="Cannot close account with positive balance")
        self.repo.delete(account)
