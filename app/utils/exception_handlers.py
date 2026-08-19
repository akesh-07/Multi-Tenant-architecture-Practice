from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.utils.exceptions import BaseCustomException

def custom_exception_handler(request: Request, exc: BaseCustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.__class__.__name__, "detail": exc.message}
    )

def add_exception_handlers(app: FastAPI):
    """Register all custom exception handlers with the FastAPI app."""
    app.add_exception_handler(BaseCustomException, custom_exception_handler)
