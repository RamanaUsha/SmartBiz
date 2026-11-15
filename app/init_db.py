from app.database import engine, Base
from app.models.customer_db import CustomerDB
from app.models.audit_log_db import AuditLogDB

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()