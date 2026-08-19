from sqlalchemy import Column, Integer, String
from app.database.base import Base

class TenantDB(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
