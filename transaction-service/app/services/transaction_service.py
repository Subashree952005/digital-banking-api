from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.account_repository import AccountRepository
from app.models.transaction import TransactionType
from app.models.account import AccountStatus
from app.schemas.transaction_schema import TransferRequest, DepositRequest, WithdrawRequest


class TransactionService:
    def __init__(self, db: Session):
        self.tx_repo = TransactionRepository(db)
        self.acc_repo = AccountRepository(db)

    def transfer(self, user_id, data: TransferRequest):
        if data.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        sender_accounts = self.acc_repo.get_by_user(user_id)
        if not sender_accounts:
            raise HTTPException(status_code=400, detail="No accounts found")
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
            raise HTTPException(status_code=400, detail="Destination account not active")
        if sender.id == receiver.id:
            raise HTTPException(status_code=400, detail="Cannot transfer to same account")
        self.acc_repo.update(sender, balance=sender.balance - data.amount)
        self.acc_repo.update(receiver, balance=receiver.balance + data.amount)
        return self.tx_repo.create(
            amount=data.amount,
            tx_type=TransactionType.transfer,
            user_id=user_id,
            from_account_id=sender.id,
            to_account_id=receiver.id,
            description=f"Transfer to {receiver.account_number}",
        )

    def deposit(self, user_id, data: DepositRequest):
        if data.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        account = self.acc_repo.get_by_id(data.account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if account.status != AccountStatus.active:
            raise HTTPException(status_code=400, detail="Account is not active")
        self.acc_repo.update(account, balance=account.balance + data.amount)
        return self.tx_repo.create(
            amount=data.amount,
            tx_type=TransactionType.deposit,
            user_id=user_id,
            to_account_id=account.id,
            description="Deposit",
        )

    def withdraw(self, user_id, data: WithdrawRequest):
        if data.amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be positive")
        account = self.acc_repo.get_by_id(data.account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        if account.status != AccountStatus.active:
            raise HTTPException(status_code=400, detail="Account is not active")
        if str(account.user_id) != str(user_id):
            raise HTTPException(status_code=403, detail="Not your account")
        if account.balance < data.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        self.acc_repo.update(account, balance=account.balance - data.amount)
        return self.tx_repo.create(
            amount=data.amount,
            tx_type=TransactionType.withdrawal,
            user_id=user_id,
            from_account_id=account.id,
            description="Withdrawal",
        )

    def get_transactions(self, user_id):
        return self.tx_repo.get_by_user(user_id)

    def delete_transaction(self, tx_id):
        tx = self.tx_repo.get_by_id(tx_id)
        if not tx:
            raise HTTPException(status_code=404, detail="Transaction not found")
        self.tx_repo.delete(tx)