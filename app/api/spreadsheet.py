
from io import BytesIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.spreadsheet_service import read_spreadsheet
from app.services.data_cleaning_service import (
    clean_whitespace,
    clean_dataframe
)
from app.services.data_quality_service import (
    generate_data_overview,
    generate_missing_value_report,
    generate_duplicate_report,
    generate_invalid_email_report,
    calculate_data_quality_score
)
from app.services.excel_export_service import export_cleaned_excel
from app.services.data_comparison_service import compare_dataframes
from app.services.audit_log_service import create_audit_log
from app.models.user_db import UserDB
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/spreadsheets",
    tags=["Spreadsheets"]
)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/upload")
async def upload_spreadsheet(
    file: UploadFile = File(...),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Upload a CSV or XLSX spreadsheet and generate
    a data quality report.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was selected"
        )

    file_extension = file.filename.lower().rsplit(".", 1)[-1]

    if file_extension not in ["csv", "xlsx"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload CSV or XLSX."
        )

    file_content = await file.read(MAX_FILE_SIZE + 1)

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the maximum limit of 5 MB"
        )

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty"
        )

    try:
        dataframe = read_spreadsheet(
            file.filename,
            file_content
        )

        if dataframe.empty or len(dataframe.columns) == 0:
            raise HTTPException(
                status_code=400,
                detail="The spreadsheet contains no data"
            )

        required_columns = ["name", "email"]

        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {missing_columns}"
            )

        cleaned_dataframe = clean_whitespace(dataframe)

        overview = generate_data_overview(cleaned_dataframe)

        missing_report = generate_missing_value_report(
            cleaned_dataframe
        )

        duplicate_report = generate_duplicate_report(
            cleaned_dataframe,
            ["email"]
        )

        invalid_email_report = generate_invalid_email_report(
            cleaned_dataframe,
            "email"
        )

        quality_score = calculate_data_quality_score(
            cleaned_dataframe,
            ["email"],
            "email"
        )

        return {
            "message": "Spreadsheet processed successfully",
            "overview": overview,
            "missing_value_report": missing_report,
            "duplicate_report": duplicate_report,
            "invalid_email_report": invalid_email_report,
            "data_quality_score": quality_score
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to process spreadsheet: {str(error)}"
        )

    finally:
        await file.close()


@router.post("/clean-and-download")
async def clean_and_download_spreadsheet(
    file: UploadFile = File(...),
    remove_duplicates: bool = False,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """
    Upload a CSV or XLSX file, clean its data,
    record the cleaning operation, and return
    the cleaned spreadsheet as an Excel download.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was selected"
        )

    file_extension = file.filename.lower().rsplit(".", 1)[-1]

    if file_extension not in ["csv", "xlsx"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload CSV or XLSX."
        )

    try:
        file_content = await file.read(MAX_FILE_SIZE + 1)

        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size exceeds the maximum limit of 5 MB"
            )

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty"
            )

        dataframe = read_spreadsheet(
            file.filename,
            file_content
        )

        if dataframe.empty or len(dataframe.columns) == 0:
            raise HTTPException(
                status_code=400,
                detail="The spreadsheet contains no data"
            )

        required_columns = ["name", "email"]

        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {missing_columns}"
            )

        cleaned_dataframe = clean_dataframe(
            dataframe,
            trim_whitespace=True,
            remove_duplicates=remove_duplicates,
            duplicate_columns=["email"] if remove_duplicates else None
        )

        comparison = compare_dataframes(
            dataframe,
            cleaned_dataframe
        )

        operations = ["trim_whitespace"]

        if remove_duplicates:
            operations.append("remove_duplicates")

        excel_content = export_cleaned_excel(cleaned_dataframe)

        create_audit_log(
            db=db,
            file_name=file.filename,
            operations=operations,
            comparison=comparison
        )

        output_file = BytesIO(excel_content)

        return StreamingResponse(
            output_file,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            headers={
                "Content-Disposition": (
                    'attachment; filename="smartbiz_cleaned.xlsx"'
                )
            }
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Unable to clean spreadsheet: {str(error)}"
        )

    finally:
        await file.close()
