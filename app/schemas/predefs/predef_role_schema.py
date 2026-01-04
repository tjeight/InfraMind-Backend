from pydantic import BaseModel


# Schema to accept the role names list
class PredefRegistrationRolePostRequestSchema(BaseModel):
    role_names: list
