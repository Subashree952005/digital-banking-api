from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_customer, get_current_admin
from app.services.transaction_service import TransactionService
from app.schemas.transaction_schema import (
    TransferRequest, DepositRequest, WithdrawRequest, TransactionResponse
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/transfer", response_model=TransactionResponse, status_code=201)
def transfer(
    data: TransferRequest,
    payload=Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return TransactionService(db).transfer(payload["sub"], data)


@router.post("/deposit", response_model=TransactionResponse, status_code=201)
def deposit(
    data: DepositRequest,
    payload=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return TransactionService(db).deposit(payload["sub"], data)


@router.post("/withdraw", response_model=TransactionResponse, status_code=201)
def withdraw(
    data: WithdrawRequest,
    payload=Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return TransactionService(db).withdraw(payload["sub"], data)


@router.get("", response_model=List[TransactionResponse])
def get_transactions(
    payload=Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return TransactionService(db).get_transactions(payload["sub"])


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: UUID,
    payload=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    TransactionService(db).delete_transaction(transaction_id)