from sqlalchemy.orm import Session
from app.schemas.student_schema import Student
from app.repositories.student_repository import StudentRepository

class StudentService:
    def __init__(self):
        self.repository = StudentRepository()

    def get_all_students(self, db: Session):
        return self.repository.get_all(db)

    def get_student(self, db: Session, student_id: int):
        return self.repository.get_by_id(db, student_id)

    def create_student(self, db: Session, student: Student):
        return self.repository.create(db, student)

    def update_student(self, db: Session, student_id: int, student: Student):
        db_student = self.repository.get_by_id(db, student_id)
        if not db_student:
            return None
        return self.repository.update(db, db_student, student)

    def delete_student(self, db: Session, student_id: int):
        db_student = self.repository.get_by_id(db, student_id)
        if not db_student:
            return False
        self.repository.delete(db, db_student)
        return True
