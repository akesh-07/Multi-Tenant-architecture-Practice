from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.student_controller import router as student_router
from app.utils.exception_handlers import add_exception_handlers
from app.core.security import create_access_token
from app.database.connection import get_db
from app.models.tenant_model import TenantDB

app = FastAPI()

add_exception_handlers(app)
app.include_router(student_router)

@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Mock Login Endpoint for testing Multitenancy.
    Enter any number in the 'username' field to represent your tenant_id (e.g. 1 or 2).
    """
    try:
        tenant_id = int(form_data.username)
    except ValueError:
        tenant_id = 1 # Fallback to default tenant if they didn't enter a number
        
    # Ensure the mock tenant actually exists in the database to prevent foreign key errors
    tenant = db.query(TenantDB).filter(TenantDB.id == tenant_id).first()
    if not tenant:
        new_tenant = TenantDB(id=tenant_id, name=f"Mock Tenant {tenant_id}")
        db.add(new_tenant)
        db.commit()

    access_token = create_access_token(data={"sub": str(tenant_id), "tenant_id": tenant_id})
    return {"access_token": access_token, "token_type": "bearer"}
