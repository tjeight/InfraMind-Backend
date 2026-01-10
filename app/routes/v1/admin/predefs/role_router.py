from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from app.configs.session import get_database
from app.dependencies.auth import get_current_admin
from app.schemas.auth.admin import AdminData
from app.schemas.predefs.predef_role_schema import (
    PredefRegistrationRolePostRequestSchema,
)
from app.services.predefs.predef_role_service import predef_registration_role_post
from app.types.db import DBSession


# configure the admin predef router
admin_predef_registration_rol_router = APIRouter()


@admin_predef_registration_rol_router.post("/roles")
async def admin_predef_registration_role_post_call(
    db: DBSession = Depends(get_database),
    payload: PredefRegistrationRolePostRequestSchema = Body(...),
    auth: AdminData = Depends(get_current_admin),
):
    # get the data
    roles = await predef_registration_role_post(db=db, payload=payload)

    # return the response
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"success": True, "data": roles}
    )
