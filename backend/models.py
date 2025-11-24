from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class CustomerRequest(Base):
    __tablename__ = "customer_requests"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
