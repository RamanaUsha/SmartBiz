import pandas as pd

from app.services.sales_service import (
    calculate_sales_revenue,
    generate_sales_summary
)

from app.services.inventory_service import (
    calculate_inventory_value,
    detect_low_stock,
    generate_inventory_summary
)


def generate_business_analytics(
    sales_dataframe: pd.DataFrame,
    inventory_dataframe: pd.DataFrame
):
    """
    Generate combined business analytics from sales
    and inventory data.
    """

    # Process sales data
    sales = calculate_sales_revenue(sales_dataframe)
    sales_summary = generate_sales_summary(sales_dataframe)

    # Identify top-selling products
    top_products = (
        sales.groupby("product_name")
        .agg(
            quantity_sold=("quantity", "sum"),
            total_revenue=("revenue", "sum")
        )
        .reset_index()
        .sort_values(
            by="quantity_sold",
            ascending=False
        )
        .head(5)
    )

    top_selling_products = [
        {
            "product_name": str(row["product_name"]),
            "quantity_sold": int(row["quantity_sold"]),
            "total_revenue": round(
                float(row["total_revenue"]), 2
            )
        }
        for _, row in top_products.iterrows()
    ]

    # Process inventory data
    inventory = calculate_inventory_value(
        inventory_dataframe
    )

    inventory_summary = generate_inventory_summary(
        inventory_dataframe
    )

    low_stock = detect_low_stock(inventory)

    low_stock_products = [
        {
            "product_id": str(row["product_id"]),
            "product_name": str(row["product_name"]),
            "quantity": int(row["quantity"]),
            "reorder_level": int(row["reorder_level"])
        }
        for _, row in low_stock.iterrows()
    ]

    return {
        "business_overview": {
            "total_revenue": sales_summary["total_revenue"],
            "total_orders": sales_summary["total_orders"],
            "total_quantity_sold": sales_summary[
                "total_quantity_sold"
            ],
            "total_products": inventory_summary[
                "total_products"
            ],
            "total_inventory_value": inventory_summary[
                "total_inventory_value"
            ],
            "low_stock_products": inventory_summary[
                "low_stock_products"
            ]
        },
        "top_selling_products": top_selling_products,
        "low_stock_alerts": low_stock_products
    }