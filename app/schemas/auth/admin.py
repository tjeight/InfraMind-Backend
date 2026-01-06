from pydantic import BaseModel, EmailStr


# Admin Schema to accept the post
class AdminSignUpRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


# Admin Schema to accept the login
class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str
