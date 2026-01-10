from pydantic import BaseModel, EmailStr

from app.types.auth import TypeUUID


# User Schema to accept the post
class UserSignUpRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    country_id: TypeUUID | None = None
    state_id: TypeUUID | None = None
    city_id: TypeUUID | None = None


# User Schema to accept the login
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


# User Schema for the dependency
class UserData(BaseModel):
    user_id: str


#  User Schema for the response
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
