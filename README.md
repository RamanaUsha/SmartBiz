
# SmartBiz – Business Data Automation Platform

SmartBiz is a Python-based business data automation and analytics platform designed to help small businesses process, clean, validate, compare, and analyze their business data.

The platform provides REST APIs and an interactive dashboard for managing customer information, processing spreadsheets, analyzing sales, monitoring inventory, and generating business insights.

## Current Features

### 1. Customer Management
- Create customer records through REST APIs.
- Validate customer names, email addresses, and Indian mobile numbers.
- Detect duplicate customer email addresses.
- Store customer records in PostgreSQL.
- Retrieve stored customer records.

### 2. Spreadsheet Processing
- Import CSV and Excel files.
- Read spreadsheet data using Pandas.
- Detect missing values.
- Clean unnecessary whitespace.
- Detect duplicate records.
- Identify invalid email addresses.
- Validate uploaded file formats and sizes.

### 3. Data Quality Analysis
- Generate spreadsheet data overview reports.
- Identify missing values.
- Generate duplicate record reports.
- Detect invalid email addresses.
- Calculate a weighted data quality score.

### 4. Advanced Data Cleaning and Excel Export
- Configure whitespace cleaning.
- Remove duplicate records.
- Fill missing values.
- Export cleaned data into Excel format.
- Preserve original spreadsheet data during processing.

### 5. Before-and-After Comparison and Audit Logs
- Compare original and cleaned spreadsheet data.
- Track original and cleaned row counts.
- Identify removed rows.
- Count modified cells.
- Record cleaning operations.
- Store audit history in PostgreSQL.
- Retrieve audit records through REST APIs.

### 6. Sales Management
- Validate sales records and required columns.
- Calculate revenue for individual sales records.
- Generate sales summaries.
- Calculate total orders.
- Calculate total quantity sold.
- Calculate total revenue and average order value.

### 7. Inventory Management
- Validate inventory records.
- Calculate individual product inventory value.
- Identify products at or below their reorder levels.
- Generate inventory summaries.
- Calculate total products, stock quantity, and inventory value.
- Generate low-stock alerts.

### 8. Business Analytics and Interactive Dashboard
- Combine sales and inventory analytics.
- Display total revenue and order counts.
- Display total quantity sold.
- Calculate total inventory value.
- Identify top five selling products.
- Generate low-stock alerts.
- Provide an interactive HTML, CSS, and JavaScript dashboard.
- Connect the dashboard directly to the FastAPI analytics endpoint.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | Database ORM |
| Pydantic | Data validation |
| Pandas | Data processing and analysis |
| OpenPyXL | Excel file processing |
| Pytest | Automated testing |
| HTTPX | API testing |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Dashboard interactions |

## Project Structure

```text
SmartBiz/
├── app/
│   ├── api/
│   │   ├── customer.py
│   │   ├── spreadsheet.py
│   │   ├── audit.py
│   │   ├── sales.py
│   │   ├── inventory.py
│   │   └── analytics.py
│   ├── models/
│   │   ├── customer.py
│   │   ├── customer_db.py
│   │   └── audit_log_db.py
│   ├── services/
│   │   ├── customer_service.py
│   │   ├── spreadsheet_service.py
│   │   ├── data_cleaning_service.py
│   │   ├── data_quality_service.py
│   │   ├── excel_export_service.py
│   │   ├── data_comparison_service.py
│   │   ├── audit_log_service.py
│   │   ├── sales_service.py
│   │   ├── inventory_service.py
│   │   └── analytics_service.py
│   ├── static/
│   │   └── index.html
│   ├── utils/
│   ├── database.py
│   ├── init_db.py
│   └── main.py
├── tests/
├── data/
├── reports/
├── docs/
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/RamanaUsha/SmartBiz.git
cd SmartBiz
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/smartbiz_db
```

Replace `YOUR_PASSWORD` with your local PostgreSQL password.

Create a PostgreSQL database named `smartbiz_db` before proceeding.

Do not commit your `.env` file to GitHub.

### 5. Initialize the Database

```powershell
python -m app.init_db
```

### 6. Start the Application

```powershell
uvicorn app.main:app --reload
```

## Application URLs

| Resource | URL |
|---|---|
| API Root | http://127.0.0.1:8000/ |
| Health Check | http://127.0.0.1:8000/health |
| Interactive API Documentation | http://127.0.0.1:8000/docs |
| Business Analytics Dashboard | http://127.0.0.1:8000/dashboard |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/customers/` | Create a customer |
| GET | `/customers/` | Retrieve customers |
| POST | `/spreadsheets/upload` | Upload and analyze a spreadsheet |
| POST | `/spreadsheets/clean-and-download` | Clean and export a spreadsheet |
| GET | `/audit-logs` | Retrieve spreadsheet audit history |
| POST | `/sales/analyze` | Analyze sales records |
| POST | `/inventory/analyze` | Analyze inventory records |
| POST | `/analytics/business-overview` | Generate combined business analytics |

## Business Analytics Dashboard

The SmartBiz dashboard provides a visual interface for analyzing business data.

### Dashboard Capabilities

- Enter sales and inventory records as JSON.
- Generate business analytics through the API.
- View total revenue and orders.
- Monitor inventory value.
- Identify top-selling products.
- Review low-stock alerts.

### Running the Dashboard

Start the FastAPI application:

```powershell
uvicorn app.main:app --reload
```

Open the dashboard:

http://127.0.0.1:8000/dashboard

The dashboard uses sample data that can be modified to test different business scenarios.

## Automated Testing

SmartBiz uses Pytest for automated service and API testing.

Run the complete test suite:

```powershell
pytest -v
```

### Current Test Results

- Total automated tests: 75
- Passed: 75
- Failed: 0

All 75 tests passed during the latest full test run.

## Development Roadmap

The following enhancements are planned for future development:

- User authentication and authorization.
- Role-based access control.
- Improved API security.
- Dashboard enhancements and visual charts.
- Docker-based deployment.
- Production deployment and monitoring.
- Additional business reporting capabilities.

## Project Status

**Completed development milestones: 8 of 10**

The project currently includes customer management, spreadsheet processing, data quality analysis, automated cleaning, audit logging, sales and inventory processing, and business analytics.

Authentication, security improvements, deployment, and further production hardening remain future development tasks.

## Author

Python Automation & Backend Development Portfolio Project.

GitHub Repository:

https://github.com/RamanaUsha/SmartBiz
