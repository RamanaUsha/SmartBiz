import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.database import Base, DATABASE_URL, get_db
from app.main import app
from app.models.customer_db import CustomerDB
from app.models.audit_log_db import AuditLogDB
from app.models.user_db import UserDB

# Use the same PostgreSQL connection, but connect to the test database.
TEST_DATABASE_URL = make_url(DATABASE_URL).set(
    database="smartbiz_test_db"
)

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(setup_test_database):
    db = TestingSessionLocal()

    db.query(AuditLogDB).delete()
    db.query(CustomerDB).delete()
    db.query(UserDB).delete()
    db.commit()

    yield db

    db.query(AuditLogDB).delete()
    db.query(CustomerDB).delete()
    db.query(UserDB).delete()
    db.commit()
    db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()