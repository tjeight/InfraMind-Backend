from uuid import UUID as _UUID

from pydantic import BaseModel

# Return the type
TypeUUID = _UUID


# User Schema for the dependency
class UserData(BaseModel):
    user_id: str
