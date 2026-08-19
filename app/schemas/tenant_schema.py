from pydantic import BaseModel

class Tenant(BaseModel):
    name: str

class TenantResponse(Tenant):
    id: int
