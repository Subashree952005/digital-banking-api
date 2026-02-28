from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_customer
from app.services.user_service import UserService
from app.schemas.user_schema import UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user=Depends(get_current_customer), db: Session = Depends(get_db)):
    return UserService(db).get_profile(current_user.id)


@router.put("/profile", response_model=UserResponse)
def update_profile(data: UserUpdateRequest, current_user=Depends(get_current_customer), db: Session = Depends(get_db)):
    return UserService(db).update_profile(current_user.id, data)


@router.delete("/profile", status_code=204)
def delete_profile(current_user=Depends(get_current_customer), db: Session = Depends(get_db)):
    UserService(db).delete_profile(current_user.id)
