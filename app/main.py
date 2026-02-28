from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router
from app.exceptions.custom_exceptions import BankingException
from app.exceptions.exception_handlers import banking_exception_handler
from app.middleware.logging_middleware import logging_middleware

app = FastAPI(
    title="Digital Banking & Loan Management API",
    description="A RESTful API for digital banking: accounts, transfers, and loan management.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
app.middleware("http")(logging_middleware)

# Exception handlers
app.add_exception_handler(BankingException, banking_exception_handler)

# Routes
app.include_router(router, prefix="/api")


@app.get("/", tags=["Health"])
def root():
    return {"message": "Digital Banking API is running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}