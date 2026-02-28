import uuid
from datetime import datetime
from sqlalchemy import Column, Float, Enum as SAEnum, DateTime, String
from sqlalchemy.types import TypeDecorator, CHAR
from app.core.database import Base
import enum


class GUID(TypeDecorator):
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        from sqlalchemy.dialects.postgresql import UUID
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)


class LoanStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    disbursed = "disbursed"
    closed = "closed"


class Loan(Base):
    __tablename__ = "loans"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(SAEnum(LoanStatus), default=LoanStatus.pending, nullable=False)
    interest_rate = Column(Float, default=8.5, nullable=False)
    duration_months = Column(Float, default=12, nullable=False)
    purpose = Column(String(500), nullable=True)
    officer_id = Column(GUID(), nullable=True)
    officer_note = Column(String(500), nullable=True)
    applied_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = Column(DateTime, nullable=True)