import pytest

from app.models.customer import CustomerCreate
from app.services.customer_service import (
    process_customer,
    get_all_customers
)


def test_process_customer(db_session):
    customer = CustomerCreate(
        name="Usha",
        email="usha@gmail.com",
        phone="9876543210",
        city="Chittoor"
    )

    result = process_customer(customer, db_session)

    assert result.name == "Usha"
    assert result.email == "usha@gmail.com"
    assert result.customer_id is not None


def test_duplicate_customer_email(db_session):
    customer1 = CustomerCreate(
        name="Usha",
        email="usha@gmail.com"
    )

    customer2 = CustomerCreate(
        name="Usha R",
        email="USHA@GMAIL.COM"
    )

    process_customer(customer1, db_session)

    with pytest.raises(ValueError):
        process_customer(customer2, db_session)


def test_get_all_customers(db_session):
    customer =CustomerCreate(
        name="Usha",
        email="usha@gmail.com"
    )

    process_customer(customer, db_session)

    customers = get_all_customers(db_session)

    assert len(customers) == 1
    assert customers[0].name == "Usha"