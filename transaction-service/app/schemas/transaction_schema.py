from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.transaction import TransactionType


class TransferRequest(BaseModel):
    to_account: str
    amount: float


class DepositRequest(BaseModel):
    account_id: UUID
    amount: float


class WithdrawRequest(BaseModel):
    account_id: UUID
    amount: float


class TransactionResponse(BaseModel):
    id: UUID
    from_account_id: UUID | None
    to_account_id: UUID | None
    amount: float
    type: TransactionType
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}