from sqlalchemy.orm import Session

from app.models.customer import CustomerCreate
from app.models.customer_db import CustomerDB


def process_customer(customer: CustomerCreate, db: Session):
    normalized_email = str(customer.email).strip().lower()

    # Check for duplicate email
    existing_customer = (
        db.query(CustomerDB)
        .filter(CustomerDB.email == normalized_email)
        .first()
    )

    if existing_customer:
        raise ValueError("A customer with this email already exists")

    # Create database record
    new_customer = CustomerDB(
        name=customer.name,
        email=normalized_email,
        phone=customer.phone,
        city=customer.city
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


def get_all_customers(db: Session):
    return db.query(CustomerDB).all()