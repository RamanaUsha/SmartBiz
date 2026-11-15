import pandas as pd

from fastapi import APIRouter, Body, Depends, HTTPException

from app.models.user_db import UserDB
from app.services.sales_service import (
    calculate_sales_revenue,
    generate_sales_summary
)
from app.utils.auth import get_current_user


router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post("/analyze")
def analyze_sales(
    records: list[dict] = Body(...),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Analyze sales records and return revenue and summary.
    Requires JWT authentication.
    """

    try:
        dataframe = pd.DataFrame(records)

        sales_data = calculate_sales_revenue(dataframe)
        summary = generate_sales_summary(dataframe)

        return {
            "message": "Sales data analyzed successfully",
            "summary": summary,
            "sales_records": sales_data.to_dict(orient="records")
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process sales data"
        )