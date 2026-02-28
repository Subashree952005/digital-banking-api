import uuid
from sqlalchemy import Column, String, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, CHAR
from app.core.database import Base
import enum


class GUID(TypeDecorator):
    """Platform-independent GUID type. Uses PostgreSQL's UUID, uses CHAR(36) for SQLite."""
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


class UserRole(str, enum.Enum):
    customer = "customer"
    officer = "officer"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SAEnum(UserRole), default=UserRole.customer, nullable=False)

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    loans = relationship(
        "Loan",
        foreign_keys="Loan.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )