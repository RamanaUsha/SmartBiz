
from io import BytesIO

import pandas as pd


def read_spreadsheet(file_name: str, file_content: bytes):
    """
    Read an Excel or CSV file and return its contents
    as a Pandas DataFrame.
    """

    file_extension = file_name.lower().rsplit(".", 1)[-1]

    if file_extension == "csv":
        dataframe = pd.read_csv(BytesIO(file_content))

    elif file_extension == "xlsx":
        dataframe = pd.read_excel(
            BytesIO(file_content),
            engine="openpyxl"
        )

    else:
        raise ValueError(
            "Unsupported file format. Please upload CSV or XLSX."
        )

    return dataframe
