import pandas as pd

from fastapi import APIRouter, Body, Depends, HTTPException

from app.models.user_db import UserDB
from app.services.inventory_service import (
    calculate_inventory_value,
    detect_low_stock,
    generate_inventory_summary
)
from app.utils.auth import get_current_user


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.post("/analyze")
def analyze_inventory(
    records: list[dict] = Body(...),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Analyze inventory records and return stock information.
    Requires JWT authentication.
    """

    try:
        dataframe = pd.DataFrame(records)

        inventory_data = calculate_inventory_value(dataframe)
        low_stock = detect_low_stock(inventory_data)
        summary = generate_inventory_summary(dataframe)

        return {
            "message": "Inventory data analyzed successfully",
            "summary": summary,
            "inventory_records": inventory_data.to_dict(
                orient="records"
            ),
            "low_stock_products": low_stock.to_dict(
                orient="records"
            )
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process inventory data"
        )