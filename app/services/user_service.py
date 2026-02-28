from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserUpdateRequest


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def get_profile(self, user_id: UUID):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_profile(self, user_id: UUID, data: UserUpdateRequest):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        updates = data.model_dump(exclude_none=True)
        if "email" in updates:
            existing = self.repo.get_by_email(updates["email"])
            if existing and existing.id != user_id:
                raise HTTPException(status_code=400, detail="Email already taken")
        return self.repo.update(user, **updates)

    def delete_profile(self, user_id: UUID):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.repo.delete(user)
