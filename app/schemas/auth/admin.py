from pydantic import BaseModel, EmailStr


# Admin Schema to accept the post
class AdminSignUpRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
