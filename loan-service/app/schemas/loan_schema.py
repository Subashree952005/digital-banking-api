from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.loan import LoanStatus


class LoanApplyRequest(BaseModel):
    amount: float
    duration_months: int = 12
    purpose: str | None = None


class LoanReviewRequest(BaseModel):
    officer_note: str | None = None


class LoanResponse(BaseModel):
    id: UUID
    user_id: UUID
    amount: float
    status: LoanStatus
    interest_rate: float
    duration_months: float
    purpose: str | None
    officer_note: str | None
    applied_at: datetime
    reviewed_at: datetime | None

    model_config = {"from_attributes": True}


class EMIResponse(BaseModel):
    loan_id: UUID
    principal: float
    interest_rate: float
    duration_months: float
    monthly_emi: float
    total_payable: float
    total_interest: float