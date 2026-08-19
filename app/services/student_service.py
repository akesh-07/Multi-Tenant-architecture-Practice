from sqlalchemy.orm import Session
from app.schemas.student_schema import Student
from app.repositories.student_repository import StudentRepository

class StudentService:
    def __init__(self):
        self.repository = StudentRepository()

    def get_all_students(self, db: Session, tenant_id: int):
        return self.repository.get_all(db, tenant_id)

    def get_student(self, db: Session, tenant_id: int, student_id: int):
        return self.repository.get_by_id(db, tenant_id, student_id)

    def create_student(self, db: Session, tenant_id: int, student: Student):
        return self.repository.create(db, tenant_id, student)

    def update_student(self, db: Session, tenant_id: int, student_id: int, student: Student):
        db_student = self.repository.get_by_id(db, tenant_id, student_id)
        if not db_student:
            return None
        return self.repository.update(db, db_student, student)

    def delete_student(self, db: Session, tenant_id: int, student_id: int):
        db_student = self.repository.get_by_id(db, tenant_id, student_id)
        if not db_student:
            return False
        self.repository.delete(db, db_student)
        return True
