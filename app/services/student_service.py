from sqlalchemy.orm import Session
from app.schemas.student_schema import Student
from app.repositories.student_repository import StudentRepository
import logging

logger = logging.getLogger(__name__)

class StudentService:
    def __init__(self):
        self.repository = StudentRepository()

    def get_all_students(self, db: Session, tenant_id: int):
        return self.repository.get_all(db, tenant_id)

    def get_student(self, db: Session, tenant_id: int, student_id: int):
        return self.repository.get_by_id(db, tenant_id, student_id)

    def create_student(self, db: Session, tenant_id: int, student: Student):
        logger.info(f"tenant={tenant_id} | Student validation passed, proceeding to repository")
        return self.repository.create(db, tenant_id, student)

    def update_student(self, db: Session, tenant_id: int, student_id: int, student: Student):
        db_student = self.repository.get_by_id(db, tenant_id, student_id)
        if not db_student:
            logger.info(f"tenant={tenant_id} | Validation failed: Student sid={student_id} not found for update")
            return None
        logger.info(f"tenant={tenant_id} | Student validation passed, proceeding to repository update")
        return self.repository.update(db, db_student, student)

    def delete_student(self, db: Session, tenant_id: int, student_id: int):
        db_student = self.repository.get_by_id(db, tenant_id, student_id)
        if not db_student:
            logger.info(f"tenant={tenant_id} | Validation failed: Student sid={student_id} not found for deletion")
            return False
        logger.info(f"tenant={tenant_id} | Student found, proceeding to repository deletion")
        self.repository.delete(db, db_student)
        return True
