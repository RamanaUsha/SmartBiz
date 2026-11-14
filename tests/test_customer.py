import pytest
from pydantic import ValidationError

from app.models.customer import CustomerCreate


def test_create_valid_customer():
    customer = CustomerCreate(
        name="Usha",
        email="usha@gmail.com",
        phone="9876543210",
        city="Chittoor"
    )

    assert customer.name == "Usha"
    assert customer.email == "usha@gmail.com"
    assert customer.phone == "9876543210"
    assert customer.city == "Chittoor"


def test_invalid_customer_email():
    with pytest.raises(ValidationError):
        CustomerCreate(
            name="Usha",
            email="invalid-email",
            phone="9876543210",
            city="Chittoor"
        )
def test_invalid_customer_phone():
    with pytest.raises(ValidationError):
       CustomerCreate(
            name="Usha",
            email="usha@gmail.com",
            phone="5123456789",
            city="Chittoor"
        )
def test_invalid_customer_name():
    with pytest.raises(ValidationError):
        CustomerCreate(
            name="A",
            email="usha@gmail.com",
            phone="9876543210",
            city="Chittoor"
        )
def test_customer_name_cannot_be_only_spaces():
    with pytest.raises(ValidationError):
        CustomerCreate(
            name="   ",
            email="usha@gmail.com",
            phone="9876543210",
            city="Chittoor"
        )