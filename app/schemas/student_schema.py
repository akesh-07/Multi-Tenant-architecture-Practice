from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    dept: str
    mail: str
