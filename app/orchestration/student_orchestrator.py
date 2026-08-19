from sqlalchemy.orm import Session
from app.schemas.student_schema import Student
from app.services.student_service import StudentService

class StudentOrchestrator:
    def __init__(self):
        self.service = StudentService()

    def get_all_students(self, db: Session):
        return self.service.get_all_students(db)

    def get_student(self, db: Session, student_id: int):
        return self.service.get_student(db, student_id)

    def create_student(self, db: Session, student: Student):
        return self.service.create_student(db, student)

    def update_student(self, db: Session, student_id: int, student: Student):
        return self.service.update_student(db, student_id, student)

    def delete_student(self, db: Session, student_id: int):
        return self.service.delete_student(db, student_id)
