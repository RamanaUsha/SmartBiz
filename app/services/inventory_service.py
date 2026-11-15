
import pandas as pd


def validate_inventory_data(dataframe: pd.DataFrame):
    """
    Validate the structure and values of inventory data.
    """

    required_columns = [
        "product_id",
        "product_name",
        "quantity",
        "unit_cost",
        "reorder_level"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if dataframe.empty:
        raise ValueError("Inventory data cannot be empty")

    if dataframe["product_id"].isna().any():
        raise ValueError("Product ID cannot be empty")

    if dataframe["product_name"].isna().any():
        raise ValueError("Product name cannot be empty")

    if dataframe["quantity"].isna().any():
        raise ValueError("Quantity cannot be empty")

    if dataframe["unit_cost"].isna().any():
        raise ValueError("Unit cost cannot be empty")

    if dataframe["reorder_level"].isna().any():
        raise ValueError("Reorder level cannot be empty")

    if (dataframe["quantity"] < 0).any():
        raise ValueError("Quantity cannot be negative")

    if (dataframe["unit_cost"] < 0).any():
        raise ValueError("Unit cost cannot be negative")

    if (dataframe["reorder_level"] < 0).any():
        raise ValueError("Reorder level cannot be negative")

    return True


def calculate_inventory_value(dataframe: pd.DataFrame):
    """
    Calculate the total value of available inventory.
    """

    validate_inventory_data(dataframe)

    result = dataframe.copy()

    result["inventory_value"] = (
        result["quantity"] * result["unit_cost"]
    )

    return result


def detect_low_stock(
    dataframe: pd.DataFrame
):
    """
    Identify products at or below their reorder level.
    """

    validate_inventory_data(dataframe)

    low_stock = dataframe[
        dataframe["quantity"] <= dataframe["reorder_level"]
    ]

    return low_stock.copy()


def generate_inventory_summary(
    dataframe: pd.DataFrame
):
    """
    Generate an overall inventory summary.
    """

    inventory = calculate_inventory_value(dataframe)

    low_stock = detect_low_stock(inventory)

    return {
        "total_products": int(len(inventory)),
        "total_stock_quantity": int(
            inventory["quantity"].sum()
        ),
        "total_inventory_value": round(
            float(inventory["inventory_value"].sum()),
            2
        ),
        "low_stock_products": int(len(low_stock))
    }
