import uuid
from sqlalchemy import Column, String, Float, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import GUID
import enum


class AccountStatus(str, enum.Enum):
    active = "active"
    frozen = "frozen"
    closed = "closed"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False, index=True)
    balance = Column(Float, default=0.0, nullable=False)
    status = Column(SAEnum(AccountStatus), default=AccountStatus.active, nullable=False)

    user = relationship("User", back_populates="accounts")
    sent_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.from_account_id",
        back_populates="from_account",
    )
    received_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.to_account_id",
        back_populates="to_account",
    )