from sqlalchemy.orm import Session
from app.schemas.student_schema import Student
from app.services.student_service import StudentService

class StudentOrchestrator:
    def __init__(self):
        self.service = StudentService()

    def get_all_students(self, db: Session, tenant_id: int):
        return self.service.get_all_students(db, tenant_id)

    def get_student(self, db: Session, tenant_id: int, student_id: int):
        return self.service.get_student(db, tenant_id, student_id)

    def create_student(self, db: Session, tenant_id: int, student: Student):
        return self.service.create_student(db, tenant_id, student)

    def update_student(self, db: Session, tenant_id: int, student_id: int, student: Student):
        return self.service.update_student(db, tenant_id, student_id, student)

    def delete_student(self, db: Session, tenant_id: int, student_id: int):
        return self.service.delete_student(db, tenant_id, student_id)
