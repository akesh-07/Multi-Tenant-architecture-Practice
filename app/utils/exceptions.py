class BaseCustomException(Exception):
    """Base class for all custom exceptions"""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

class StudentNotFoundError(BaseCustomException):
    def __init__(self, message: str = "Student not found"):
        super().__init__(message=message, status_code=404)

class DatabaseError(BaseCustomException):
    def __init__(self, message: str = "An error occurred with the database"):
        super().__init__(message=message, status_code=500)
