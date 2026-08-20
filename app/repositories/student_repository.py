from sqlalchemy.orm import Session
from app.models.student_model import StudentDB
from app.schemas.student_schema import Student
from app.utils.exceptions import DatabaseError
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class StudentRepository:
    def get_all(self, db: Session, tenant_id: int):
        # Fetch all students strictly belonging to the given tenant
        logger.debug(f"tenant={tenant_id} | Executing SELECT for all students")
        return db.query(StudentDB).filter(StudentDB.tenant_id == tenant_id).all()

    def get_by_id(self, db: Session, tenant_id: int, student_id: int):
        logger.debug(f"tenant={tenant_id} | Executing SELECT for student_id={student_id}")
        return db.query(StudentDB).filter(
            StudentDB.id == student_id,
            StudentDB.tenant_id == tenant_id
        ).first()

    def create(self, db: Session, tenant_id: int, student: Student):
        new_student = StudentDB(
            tenant_id=tenant_id,
            name=student.name,
            age=student.age,
            dept=student.dept,
            mail=student.mail
        )
        db.add(new_student)
        logger.debug(f"tenant={tenant_id} | Committing new student to database")
        try:
            db.commit()
            db.refresh(new_student)
            return new_student
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error during create: {e}")
            raise DatabaseError("Failed to create student due to a database error")

    def update(self, db: Session, db_student: StudentDB, student: Student):
        db_student.name = student.name
        db_student.age = student.age
        db_student.dept = student.dept
        db_student.mail = student.mail
        logger.debug(f"tenant={db_student.tenant_id} | Committing student_id={db_student.id} update to database")
        try:
            db.commit()
            db.refresh(db_student)
            return db_student
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error during update: {e}")
            raise DatabaseError("Failed to update student due to a database error")

    def delete(self, db: Session, db_student: StudentDB):
        logger.debug(f"tenant={db_student.tenant_id} | Deleting student_id={db_student.id} from database")
        try:
            db.delete(db_student)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error during delete: {e}")
            raise DatabaseError("Failed to delete student due to a database error")
