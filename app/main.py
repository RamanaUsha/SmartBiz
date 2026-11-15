from fastapi import FastAPI

from app.api.customer import router as customer_router
from app.api.spreadsheet import router as spreadsheet_router
from app.api.audit import router as audit_router
from app.api.sales import router as sales_router
from app.api.inventory import router as inventory_router
from app.api.analytics import router as analytics_router
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.auth import router as auth_router

app = FastAPI(
    title="SmartBiz API",
    description="Business Data Automation Platform",
    version="1.0.0"
)

app.include_router(customer_router)
app.include_router(spreadsheet_router)
app.include_router(audit_router)
app.include_router(sales_router)
app.include_router(inventory_router)
app.include_router(analytics_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to SmartBiz!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


@app.get("/dashboard", include_in_schema=False)
def dashboard():
    return FileResponse(BASE_DIR / "static" / "index.html")