import uuid
from sqlalchemy import Column, String, Float, Enum as SAEnum
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


class AccountStatus(str, enum.Enum):
    active = "active"
    frozen = "frozen"
    closed = "closed"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), nullable=False)
    account_number = Column(String(20), unique=True, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    status = Column(SAEnum(AccountStatus), default=AccountStatus.active, nullable=False)