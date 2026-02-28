import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

SQLALCHEMY_TEST_URL = "sqlite:///./test_account.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

TEST_USER_ID = str(uuid.uuid4())
TEST_ADMIN_ID = str(uuid.uuid4())

MOCK_CUSTOMER = {"sub": TEST_USER_ID, "role": "customer"}
MOCK_ADMIN = {"sub": TEST_ADMIN_ID, "role": "admin"}


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def customer_token(client):
    from app.core.dependencies import get_current_user, get_current_customer
    app.dependency_overrides[get_current_user] = lambda: MOCK_CUSTOMER
    app.dependency_overrides[get_current_customer] = lambda: MOCK_CUSTOMER
    yield "mock-token"


@pytest.fixture
def admin_token(client):
    from app.core.dependencies import get_current_user, get_current_admin
    app.dependency_overrides[get_current_user] = lambda: MOCK_ADMIN
    app.dependency_overrides[get_current_admin] = lambda: MOCK_ADMIN
    yield "mock-token"