from sqlalchemy import Column, Integer, String
from app.database.base import Base

class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    dept = Column(String)
    mail = Column(String)
