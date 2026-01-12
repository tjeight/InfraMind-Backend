from pydantic import BaseModel
from enum import Enum
from app.types.auth import TypeUUID


#  Enum for the environment types
class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


# Schema to accept the service details
class ServiceRegisterRequest(BaseModel):
    company_id: str
    name: str
    base_url: str
    scope_path: str | None = None
    environment: EnvironmentType


# Schema to update the service details
class ServiceUpdateRequest(BaseModel):
    service_id: TypeUUID
    name: str | None = None
    base_url: str | None = None
    scope_path: str | None = None
    environment: EnvironmentType | None = None
    is_active: bool | None = None


# Schema to delte the service
class ServiceDeleteRequest(BaseModel):
    service_id: str
    company_id: str
