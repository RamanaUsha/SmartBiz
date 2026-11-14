
import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    phone: Optional[str] = None
    city: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Customer name cannot be empty")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value

        if not re.fullmatch(r"[6-9]\d{9}", value):
            raise ValueError(
                "Phone number must be a valid 10-digit Indian mobile number"
            )

        return value

    @field_validator("city")
    @classmethod
    def validate_city(cls, value):
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    city: Optional[str] = None


class CustomerListResponse(BaseModel):
    total_customers: int
    customers: list[CustomerResponse]


class CustomerCreateResponse(BaseModel):
    message: str
    customer: CustomerResponse
