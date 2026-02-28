from fastapi import APIRouter
from app.api.routes import auth, users, accounts, transactions, loans, admin

router = APIRouter()
router.include_router(auth.router)
router.include_router(users.router)
router.include_router(accounts.router)
router.include_router(transactions.router)
router.include_router(loans.router)
router.include_router(admin.router)