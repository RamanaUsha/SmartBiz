from sqlalchemy import Column, Integer, String

from app.database import Base


class CustomerDB(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(10), nullable=True)
    city = Column(String(100), nullable=True)