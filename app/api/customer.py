from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import (
    CustomerCreate,
    CustomerListResponse,
    CustomerCreateResponse
)
from app.services.customer_service import (
    process_customer,
    get_all_customers
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/",
    status_code=201,
    response_model=CustomerCreateResponse,
    summary="Create a new customer",
    description="Validates customer details, checks duplicate emails, and creates a customer record.",
    responses={
        409: {"description": "A customer with this email already exists"}
    }
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    try:
        processed_customer = process_customer(customer, db)

        return {
            "message": "Customer data received successfully",
            "customer": processed_customer
        }

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.get("/", response_model=CustomerListResponse)
def list_customers(db: Session = Depends(get_db)):
    customers = get_all_customers(db)

    return {
        "total_customers": len(customers),
        "customers": customers
    }