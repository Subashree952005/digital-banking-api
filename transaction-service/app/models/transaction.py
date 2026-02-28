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


class TransactionType(str, enum.Enum):
    transfer = "transfer"
    deposit = "deposit"
    withdrawal = "withdrawal"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    from_account_id = Column(GUID(), nullable=True)
    to_account_id = Column(GUID(), nullable=True)
    user_id = Column(GUID(), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(SAEnum(TransactionType), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)