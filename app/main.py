from fastapi import FastAPI

from app.api.customer import router as customer_router
from app.api.spreadsheet import router as spreadsheet_router
from app.api.audit import router as audit_router

app = FastAPI(
    title="SmartBiz API",
    description="Business Data Automation Platform",
    version="1.0.0"
)

app.include_router(customer_router)
app.include_router(spreadsheet_router)
app.include_router(audit_router)

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