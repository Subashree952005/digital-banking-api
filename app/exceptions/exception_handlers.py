from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import BankingException


async def banking_exception_handler(request: Request, exc: BankingException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )