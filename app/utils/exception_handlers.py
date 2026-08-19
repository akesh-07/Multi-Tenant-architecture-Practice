import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from app.utils.exceptions import BaseCustomException

logger = logging.getLogger(__name__)

def custom_exception_handler(request: Request, exc: BaseCustomException):
    logger.warning(f"Custom Exception: {exc.__class__.__name__} - {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.__class__.__name__, "detail": exc.message}
    )

def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled Exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": "An unexpected error occurred."}
    )

def add_exception_handlers(app: FastAPI):
    """Register all custom exception handlers with the FastAPI app."""
    app.add_exception_handler(BaseCustomException, custom_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
