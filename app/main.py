from fastapi import FastAPI
from app.api.student_controller import router as student_router
from app.utils.exception_handlers import add_exception_handlers

app = FastAPI()

add_exception_handlers(app)
app.include_router(student_router)
