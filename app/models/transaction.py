import uuid
from datetime import datetime
from sqlalchemy import Column, Float, Enum as SAEnum, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import GUID
import enum


class TransactionType(str, enum.Enum):
    transfer = "transfer"
    deposit = "deposit"
    withdrawal = "withdrawal"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    from_account_id = Column(GUID(), ForeignKey("accounts.id"), nullable=True)
    to_account_id = Column(GUID(), ForeignKey("accounts.id"), nullable=True)
    amount = Column(Float, nullable=False)
    type = Column(SAEnum(TransactionType), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    from_account = relationship(
        "Account",
        foreign_keys=[from_account_id],
        back_populates="sent_transactions",
    )
    to_account = relationship(
        "Account",
        foreign_keys=[to_account_id],
        back_populates="received_transactions",
    )