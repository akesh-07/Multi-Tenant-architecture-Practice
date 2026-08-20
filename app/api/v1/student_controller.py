from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.student_schema import Student
from app.orchestration.student_orchestrator import StudentOrchestrator
from app.utils.exceptions import StudentNotFoundError
from app.dependencies.tenant import get_current_tenant
import logging

logger = logging.getLogger(__name__)
# Router handles HTTP routing while delegating business logic to the orchestrator
router = APIRouter()
orchestrator = StudentOrchestrator()

@router.post("/students")
def create_student(student: Student, db: Session = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    """
    Description

    Create a new student.

    Request Body / Parameters:
    - student: The details of the student to create.

    Returns:
    - The created student object.
    - HTTP status code 200 on success.
    """
    logger.info(f"tenant={tenant_id} | Creating new student")
    return orchestrator.create_student(db, tenant_id, student)

@router.get("/students")
def get_students(db: Session = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
    """
    Description

    Retrieve a list of all students.

    Request Body / Parameters:
    - None

    Returns:
    - A list of all students.
    - HTTP status code 200 on success.
    """
    logger.info(f"tenant={tenant_id} | Fetching all students")
    return orchestrator.get_all_students(db, tenant_id)

@router.get("/students/{sid}")
def get_student(sid: int, db: Session = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
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
    logger.info(f"tenant={tenant_id} | Fetching student sid={sid}")
    student = orchestrator.get_student(db, tenant_id, sid)
    if not student:
        logger.warning(f"tenant={tenant_id} | Student sid={sid} not found")
        raise StudentNotFoundError()
    return student

@router.put("/students/{sid}")
def update_student(sid: int, student: Student, db: Session = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
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
    logger.info(f"tenant={tenant_id} | Updating student sid={sid}")
    updated_student = orchestrator.update_student(db, tenant_id, sid, student)
    if not updated_student:
        logger.warning(f"tenant={tenant_id} | Student sid={sid} not found for update")
        raise StudentNotFoundError()
    return updated_student

@router.delete("/students/{sid}")
def delete_student(sid: int, db: Session = Depends(get_db), tenant_id: int = Depends(get_current_tenant)):
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
    logger.info(f"tenant={tenant_id} | Deleting student sid={sid}")
    success = orchestrator.delete_student(db, tenant_id, sid)
    if not success:
        logger.warning(f"tenant={tenant_id} | Student sid={sid} not found for deletion")
        raise StudentNotFoundError()
    return {"message": "Student deleted"}
