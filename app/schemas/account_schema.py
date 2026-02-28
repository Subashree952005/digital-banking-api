from pydantic import BaseModel
from uuid import UUID
from app.models.account import AccountStatus


class CreateAccountRequest(BaseModel):
    initial_deposit: float = 0.0


class AccountResponse(BaseModel):
    id: UUID
    account_number: str
    balance: float
    status: AccountStatus

    model_config = {"from_attributes": True}


class AccountUpdateRequest(BaseModel):
    status: AccountStatus | None = None
