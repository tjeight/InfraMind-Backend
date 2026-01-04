from fastapi import APIRouter, status

from app.types.db import DBSession


# configure the router
router = APIRouter()



@router.post("/signup")
async def admin_signup(db:DBSession,payload:payload)
