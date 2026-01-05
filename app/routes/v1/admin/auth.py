from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.auth.admin import AdminSignUpRequest
from app.types.db import DBSession
from app.services.auth.admin import signup_admin

# configure the router
router = APIRouter()


@router.post("/signup")
async def admin_signup(db: DBSession, payload: AdminSignUpRequest):
    # get the admin
    admin = await signup_admin(db=db, payload=payload)

    # return the admin

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"success": "True", "message": "Admin Created Successfully"},
    )
