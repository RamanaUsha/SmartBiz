import pandas as pd

from fastapi import APIRouter, Body, Depends, HTTPException

from app.models.user_db import UserDB
from app.services.analytics_service import (
    generate_business_analytics
)
from app.utils.auth import get_current_user


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.post("/business-overview")
def business_overview(
    payload: dict = Body(...),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Generate combined business analytics
    from sales and inventory records.
    Requires JWT authentication.
    """

    try:
        if "sales" not in payload or "inventory" not in payload:
            raise ValueError(
                "Both sales and inventory data are required"
            )

        if not isinstance(payload["sales"], list):
            raise ValueError("Sales data must be a list")

        if not isinstance(payload["inventory"], list):
            raise ValueError("Inventory data must be a list")

        sales_dataframe = pd.DataFrame(payload["sales"])
        inventory_dataframe = pd.DataFrame(payload["inventory"])

        analytics = generate_business_analytics(
            sales_dataframe,
            inventory_dataframe
        )

        return {
            "message": "Business analytics generated successfully",
            **analytics
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )