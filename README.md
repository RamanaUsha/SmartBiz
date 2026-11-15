
# SmartBiz – Business Data Automation Platform

SmartBiz is a Python-based business data automation project designed to help small businesses manage and validate customer information through REST APIs.

## Current Features

- Create customer records through a REST API.
- Validate customer names, email addresses, and Indian mobile numbers.
- Detect duplicate customer email addresses.
- Store customer records in PostgreSQL.
- Retrieve all stored customer records.
- Separate API, service, database, and validation layers.
- Automated tests using Pytest.

## Technology Stack

- **Language:** Python
- **API Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Testing:** Pytest
- **Excel Processing:** Pandas, OpenPyXL

## Project Structure

```text
SmartBiz/
├── app/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── database.py
│   ├── init_db.py
│   └── main.py
├── tests/
├── data/
├── reports/
├── docs/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd SmartBiz
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/smartbiz_db
```

Replace `YOUR_PASSWORD` with your local PostgreSQL password.

Create the PostgreSQL database named `smartbiz_db` before proceeding.

### 5. Create database tables

```powershell
python -m app.init_db
```

### 6. Start the API server

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/customers/` | Create a customer |
| GET | `/customers/` | Retrieve all customers |

## Run Automated Tests

```powershell
pytest -v
```

The project includes validation, service, and API tests.

## Development Status

The current implementation includes customer validation, duplicate detection, PostgreSQL persistence, REST API endpoints, and automated tests.

Planned enhancements include:

- Excel and CSV data import.
- Automated spreadsheet cleaning.
- Data quality scoring.
- Duplicate detection in business datasets.
- Data cleaning reports and exports.
- Business analytics dashboard.

## Author

Python Automation & Backend Development Portfolio Project.

## Before-and-After Comparison and Audit Logs

SmartBiz now supports:

- Comparing original and cleaned spreadsheet data.
- Counting original and cleaned rows.
- Tracking rows removed during cleaning.
- Counting modified cells.
- Recording cleaning operations performed on each spreadsheet.
- Saving audit records in PostgreSQL.
- Retrieving audit history through the `GET /audit-logs` API.

### Spreadsheet Cleaning and Audit

The `POST /spreadsheets/clean-and-download` endpoint cleans an uploaded CSV or Excel file and returns the cleaned data as an Excel file.

It also creates an audit record containing:
- Original filename
- Cleaning operations
- Original row count
- Cleaned row count
- Removed row count
- Modified cell count
- Audit timestamp

### View Audit History

Use:

`GET /audit-logs`

This endpoint returns the saved spreadsheet cleaning history.

## Sales and Inventory Management

SmartBiz now supports sales and inventory data processing.

### Sales Features
- Validate sales data and required columns.
- Calculate revenue for individual sales records.
- Generate sales summaries.
- Calculate total orders, quantity sold, total revenue, and average order value.
- REST API endpoint: `POST /sales/analyze`

### Inventory Features
- Validate inventory data and required columns.
- Calculate individual product inventory value.
- Identify products at or below their reorder level.
- Generate inventory summaries.
- Calculate total products, stock quantity, inventory value, and low-stock product count.
- REST API endpoint: `POST /inventory/analyze`

### Testing
Sales and inventory services and APIs include automated tests.
