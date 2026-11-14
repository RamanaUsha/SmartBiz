
from io import BytesIO

import pandas as pd


def export_cleaned_excel(dataframe: pd.DataFrame) -> bytes:
    """
    Convert a cleaned DataFrame into an Excel file.

    Returns the Excel file as bytes so FastAPI
    can send it as a downloadable response.
    """

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:
        dataframe.to_excel(
            writer,
            index=False,
            sheet_name="Cleaned Data"
        )

    output.seek(0)

    return output.getvalue()
