
import pandas as pd


def validate_sales_data(dataframe: pd.DataFrame):
    """
    Validate the structure and required fields of sales data.
    """

    required_columns = [
        "order_id",
        "product_name",
        "quantity",
        "unit_price"
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
        raise ValueError("Sales data cannot be empty")

    if dataframe["order_id"].isna().any():
        raise ValueError("Order ID cannot be empty")

    if dataframe["product_name"].isna().any():
        raise ValueError("Product name cannot be empty")

    if dataframe["quantity"].isna().any():
        raise ValueError("Quantity cannot be empty")

    if dataframe["unit_price"].isna().any():
        raise ValueError("Unit price cannot be empty")

    if (dataframe["quantity"] <= 0).any():
        raise ValueError("Quantity must be greater than zero")

    if (dataframe["unit_price"] < 0).any():
        raise ValueError("Unit price cannot be negative")

    return True


def calculate_sales_revenue(dataframe: pd.DataFrame):
    """
    Calculate revenue for every sales record.
    """

    validate_sales_data(dataframe)

    result = dataframe.copy()

    result["revenue"] = (
        result["quantity"] * result["unit_price"]
    )

    return result


def generate_sales_summary(dataframe: pd.DataFrame):
    """
    Generate an overall sales summary.
    """

    sales_data = calculate_sales_revenue(dataframe)

    return {
        "total_orders": int(len(sales_data)),
        "total_quantity_sold": int(
            sales_data["quantity"].sum()
        ),
        "total_revenue": round(
            float(sales_data["revenue"].sum()),
            2
        ),
        "average_order_value": round(
            float(sales_data["revenue"].mean()),
            2
        )
    }
