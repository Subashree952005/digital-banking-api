from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.account_repository import AccountRepository
from app.models.transaction import TransactionType
from app.models.account import AccountStatus
from app.schemas.transaction_schema import TransferRequest, DepositRequest, WithdrawRequest


class TransactionService:
    def __init__(self, db: Session):
        self.tx_repo = TransactionRepository(db)
        self.acc_repo = AccountRepository(db)
        self.db = db

    def _get_active_account(self, account_id: UUID):
        account = self.acc_repo.get_by_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if account.status != AccountStatus.active:
            raise HTTPException(status_code=400, detail=f"Account is {account.status.value}")
        return account

    def transfer(self, user_id: UUID, data: TransferRequest):
        if data.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        sender_accounts = self.acc_repo.get_by_user(user_id)
        if not sender_accounts:
            raise HTTPException(status_code=400, detail="No accounts found for user")
        sender = None
        for acc in sender_accounts:
            if acc.status == AccountStatus.active and acc.balance >= data.amount:
                sender = acc
                break
        if not sender:
            raise HTTPException(status_code=400, detail="Insufficient funds or no active account")
        receiver = self.acc_repo.get_by_number(data.to_account)
        if not receiver:
            raise HTTPException(status_code=404, detail="Destination account not found")
        if receiver.status != AccountStatus.active:
            raise HTTPException(status_code=400, detail="Destination account is not active")
        if sender.id == receiver.id:
            raise HTTPException(status_code=400, detail="Cannot transfer to same account")
        self.acc_repo.update(sender, balance=sender.balance - data.amount)
        self.acc_repo.update(receiver, balance=receiver.balance + data.amount)
        return self.tx_repo.create(
            amount=data.amount,
            tx_type=TransactionType.transfer,
            from_account_id=sender.id,
            to_account_id=receiver.id,
            description=f"Transfer to {receiver.account_number}",
        )

    def deposit(self, data: DepositRequest):
        if data.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        account = self._get_active_account(data.account_id)
        self.acc_repo.update(account, balance=account.balance + data.amount)
        return self.tx_repo.create(
            amount=data.amount,
            tx_type=TransactionType.deposit,
            to_account_id=account.id,
            description="Deposit",
        )

    def withdraw(self, user_id: UUID, data: WithdrawRequest):
        if data.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        account = self._get_active_account(data.account_id)
        if account.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not your account")
        if account.balance < data.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        self.acc_repo.update(account, balance=account.balance - data.amount)
        return self.tx_repo.create(
            amount=data.amount,
            tx_type=TransactionType.withdrawal,
            from_account_id=account.id,
            description="Withdrawal",
        )

    def get_transactions(self, user_id: UUID):
        accounts = self.acc_repo.get_by_user(user_id)
        txs = []
        seen = set()
        for acc in accounts:
            for tx in self.tx_repo.get_by_account(acc.id):
                if tx.id not in seen:
                    seen.add(tx.id)
                    txs.append(tx)
        txs.sort(key=lambda t: t.created_at, reverse=True)
        return txs

    def delete_transaction(self, tx_id: UUID):
        tx = self.tx_repo.get_by_id(tx_id)
        if not tx:
            raise HTTPException(status_code=404, detail="Transaction not found")
        self.tx_repo.delete(tx)
