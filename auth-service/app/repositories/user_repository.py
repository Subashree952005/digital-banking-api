from sqlalchemy.orm import Session
from app.models.user import User, UserRole


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, email: str, full_name: str, password_hash: str, role=None) -> User:
        user = User(
            email=email,
            full_name=full_name,
            password_hash=password_hash,
            role=role or UserRole.customer,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user