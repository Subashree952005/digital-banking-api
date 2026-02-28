from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.accounts import router

app = FastAPI(
    title="Account Service",
    description="Bank Account Management Service",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/health", tags=["Health"])
def health():
    return {"service": "account-service", "status": "running"}