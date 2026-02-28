import uuid
from datetime import datetime
from sqlalchemy import Column, Float, Enum as SAEnum, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import GUID
import enum


class LoanStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    disbursed = "disbursed"
    closed = "closed"


class Loan(Base):
    __tablename__ = "loans"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(SAEnum(LoanStatus), default=LoanStatus.pending, nullable=False)
    interest_rate = Column(Float, default=8.5, nullable=False)
    duration_months = Column(Float, default=12, nullable=False)
    purpose = Column(String(500), nullable=True)
    officer_id = Column(GUID(), ForeignKey("users.id"), nullable=True)
    officer_note = Column(String(500), nullable=True)
    applied_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = Column(DateTime, nullable=True)

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="loans",
    )
    officer = relationship(
        "User",
        foreign_keys=[officer_id],
    )