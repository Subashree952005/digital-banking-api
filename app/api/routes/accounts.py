from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_customer, get_current_admin, get_current_user
from app.services.account_service import AccountService
from app.schemas.account_schema import CreateAccountRequest, AccountResponse, AccountUpdateRequest

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("", response_model=AccountResponse, status_code=201)
def create_account(
    data: CreateAccountRequest,
    current_user=Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return AccountService(db).create_account(current_user.id, data)


@router.get("", response_model=List[AccountResponse])
def list_accounts(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AccountService(db).get_user_accounts(current_user.id)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AccountService(db).get_account(account_id, current_user.id)


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: UUID,
    data: AccountUpdateRequest,
    current_user=Depends(get_current_customer),
    db: Session = Depends(get_db),
):
    return AccountService(db).update_account(account_id, current_user.id, data)


@router.put("/{account_id}/freeze", response_model=AccountResponse)
def freeze_account(
    account_id: UUID,
    current_user=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return AccountService(db).freeze_account(account_id)


@router.delete("/{account_id}", status_code=204)
def delete_account(
    account_id: UUID,
    current_user=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    AccountService(db).close_account(account_id)