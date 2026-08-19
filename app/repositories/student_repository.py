from sqlalchemy.orm import Session
from app.models.student_model import StudentDB
from app.schemas.student_schema import Student

class StudentRepository:
    def get_all(self, db: Session, tenant_id: int):
        return db.query(StudentDB).filter(StudentDB.tenant_id == tenant_id).all()

    def get_by_id(self, db: Session, tenant_id: int, student_id: int):
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
        db.commit()
        db.refresh(new_student)
        return new_student

    def update(self, db: Session, db_student: StudentDB, student: Student):
        db_student.name = student.name
        db_student.age = student.age
        db_student.dept = student.dept
        db_student.mail = student.mail
        db.commit()
        db.refresh(db_student)
        return db_student

    def delete(self, db: Session, db_student: StudentDB):
        db.delete(db_student)
        db.commit()
