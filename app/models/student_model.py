from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base
from app.models.tenant_model import TenantDB

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String)
    age = Column(Integer)
    dept = Column(String)
    mail = Column(String)
