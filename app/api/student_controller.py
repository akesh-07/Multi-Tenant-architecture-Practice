from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.student_schema import Student
from app.orchestration.student_orchestrator import StudentOrchestrator
from app.utils.exceptions import StudentNotFoundError

router = APIRouter()
orchestrator = StudentOrchestrator()

@router.post("/students")
def create_student(student: Student, db: Session = Depends(get_db)):
    """
    Description

    Create a new student.

    Request Body / Parameters:
    - student: The details of the student to create.

    Returns:
    - The created student object.
    - HTTP status code 200 on success.
    """
    return orchestrator.create_student(db, student)

@router.get("/students")
def get_students(db: Session = Depends(get_db)):
    """
    Description

    Retrieve a list of all students.

    Request Body / Parameters:
    - None

    Returns:
    - A list of all students.
    - HTTP status code 200 on success.
    """
    return orchestrator.get_all_students(db)

@router.get("/students/{sid}")
def get_student(sid: int, db: Session = Depends(get_db)):
    """
    Description

    Retrieve a student by ID.

    Request Body / Parameters:
    - sid: Unique identifier of the student.

    Returns:
    - Student details if found.
    - HTTP status code 200 on success.
    - HTTP status code 404 if the student does not exist.
    """
    student = orchestrator.get_student(db, sid)
    if not student:
        raise StudentNotFoundError()
    return student

@router.put("/students/{sid}")
def update_student(sid: int, student: Student, db: Session = Depends(get_db)):
    """
    Description

    Update an existing student by ID.

    Request Body / Parameters:
    - sid: Unique identifier of the student.
    - student: The updated student details.

    Returns:
    - The updated student object.
    - HTTP status code 200 on success.
    - HTTP status code 404 if the student does not exist.
    """
    updated_student = orchestrator.update_student(db, sid, student)
    if not updated_student:
        raise StudentNotFoundError()
    return updated_student

@router.delete("/students/{sid}")
def delete_student(sid: int, db: Session = Depends(get_db)):
    """
    Description

    Delete a student by ID.

    Request Body / Parameters:
    - sid: Unique identifier of the student.

    Returns:
    - A success message confirming deletion.
    - HTTP status code 200 on success.
    - HTTP status code 404 if the student does not exist.
    """
    success = orchestrator.delete_student(db, sid)
    if not success:
        raise StudentNotFoundError()
    return {"message": "Student deleted"}
