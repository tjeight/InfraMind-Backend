from pydantic import BaseModel
from app.types.auth import TypeUUID


# Schema for a single company item
class CompanyRegisterRequest(BaseModel):
    company_name: str
    company_slug: str
    company_website: str | None = None
    is_active: bool | None = True


# Schema for list of companies
class CompanyUpdateRequest(BaseModel):
    company_id: TypeUUID
    company_name: str | None = None
    company_slug: str | None = None
    company_website: str | None = None

    is_active: bool | None = None


# Schema for delete the companies
class CompanyDeleteRequest(BaseModel):
    company_id: list[TypeUUID]
