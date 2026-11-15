
# SmartBiz - Business Data Automation Platform

SmartBiz is a Python-based business data automation and analytics platform designed to help small businesses process, clean, validate, compare, and analyze their business data.

The platform provides REST APIs and an interactive dashboard for managing customer information, processing spreadsheets, analyzing sales, monitoring inventory, and generating business insights.

## Current Features

### 1. Customer Management
- Create customer records through REST APIs.
- Validate customer names, email addresses, and Indian mobile numbers.
- Detect duplicate customer email addresses.
- Store customer records in PostgreSQL.
- Retrieve stored customer records.
- Protect customer endpoints using JWT authentication.

### 2. Spreadsheet Processing
- Import CSV and Excel files.
- Read spreadsheet data using Pandas.
- Detect missing values.
- Clean unnecessary whitespace.
- Detect duplicate records.
- Identify invalid email addresses.
- Validate uploaded file formats and sizes.
- Require authentication for spreadsheet operations.

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
- Retrieve audit records through protected REST APIs.

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
- Identify the top five selling products.
- Generate low-stock alerts.
- Provide an interactive HTML, CSS, and JavaScript dashboard.
- Connect the dashboard directly to the FastAPI analytics endpoint.

### 9. Authentication and Security
- Register new users.
- Authenticate users through email and password.
- Hash passwords using Argon2.
- Generate and validate JSON Web Tokens (JWT).
- Provide a protected account endpoint.
- Protect customer, spreadsheet, audit, sales, inventory, and analytics APIs.
- Integrate login, registration, and logout into the dashboard.
- Require a valid bearer token for protected API operations.

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
| PyJWT | JWT authentication |
| pwdlib | Password hashing |
| Argon2 | Secure password hashing algorithm |
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
│   │   ├── analytics.py
│   │   └── auth.py
│   ├── models/
│   │   ├── customer.py
│   │   ├── customer_db.py
│   │   ├── audit_log_db.py
│   │   ├── user.py
│   │   └── user_db.py
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
│   │   ├── analytics_service.py
│   │   └── auth_service.py
│   ├── static/
│   │   └── index.html
│   ├── utils/
│   │   └── auth.py
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

```powershell
git clone https://github.com/RamanaUsha/SmartBiz.git
cd SmartBiz
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Add the following configuration:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/smartbiz_db

JWT_SECRET_KEY=YOUR_GENERATED_SECRET
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secure JWT secret locally using:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copy the generated value into `JWT_SECRET_KEY` in your local `.env` file.

Replace `YOUR_PASSWORD` with your local PostgreSQL password.

Create a PostgreSQL database named `smartbiz_db` before proceeding.

**Security:** Never commit your `.env` file or share your database password or JWT secret.

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

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate and receive a JWT |
| GET | `/auth/me` | Retrieve the authenticated user's account |

### Business APIs

All business API endpoints below require a valid bearer token.

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

## Authentication Workflow

1. Register a user using `POST /auth/register`.
2. Log in using `POST /auth/login`.
3. Receive an access token.
4. Include the token in protected API requests:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

5. Access the protected account endpoint using `GET /auth/me`.

Access tokens expire according to `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.

The dashboard keeps the access token in memory. Refreshing the page requires logging in again.

## Business Analytics Dashboard

The SmartBiz dashboard provides a visual interface for analyzing business data.

### Dashboard Capabilities

- Register and log in.
- Enter sales and inventory records as JSON.
- Generate business analytics through the authenticated API.
- View total revenue and orders.
- Monitor inventory value.
- Identify top-selling products.
- Review low-stock alerts.
- Log out of the dashboard.

### Running the Dashboard

Start the FastAPI application:

```powershell
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000/dashboard

The dashboard uses sample data that can be modified to test different business scenarios.

## Automated Testing

SmartBiz uses Pytest for automated service and API testing.

Run the complete test suite:

```powershell
pytest -v
```

### Latest Test Results

- Total automated tests: 93
- Passed: 93
- Failed: 0

All 93 tests passed during the latest full test run.

A non-blocking Starlette deprecation warning related to HTTPX and TestClient was observed during testing.

## Development Roadmap

| Milestone | Description | Status |
|---|---|---|
| 1 | Customer API and database | Completed |
| 2 | Spreadsheet reading and cleaning | Completed |
| 3 | Data quality reporting | Completed |
| 4 | Spreadsheet upload API | Completed |
| 5 | Advanced cleaning and Excel export | Completed |
| 6 | Data comparison and audit logs | Completed |
| 7 | Sales and inventory processing | Completed |
| 8 | Business analytics and dashboard | Completed |
| 9 | Authentication and security improvements | Completed |
| 10 | Deployment, documentation, and portfolio preparation | In progress |

## Project Status

**Completed development milestones: 9 of 10 (90% of the proposed roadmap).**

SmartBiz currently includes customer management, spreadsheet processing, data quality analysis, automated cleaning, audit logging, sales and inventory processing, business analytics, an interactive dashboard, and JWT-based authentication.

Deployment and additional production-readiness improvements remain to be completed.

## Future Improvements

- Role-based access control.
- Password reset and account recovery.
- Rate limiting and additional API security.
- Improved dashboard charts and reporting.
- Docker-based deployment.
- Production deployment and monitoring.
- Additional business reporting capabilities.

## Author

Python Automation & Backend Development Portfolio Project.

GitHub Repository:

https://github.com/RamanaUsha/SmartBiz
