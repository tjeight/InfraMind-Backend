from fastapi import APIRouter, Body, Depends, Form, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.settings import settings
from app.schemas.auth.admin import AdminLoginRequest, AdminSignUpRequest
from app.services.auth.admin import login_admin, refresh_admin_token, signup_admin
from app.types.db import DBSession
from app.configs.session import get_database

# Configure router
router = APIRouter(prefix="/admin", tags=["Admin Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def admin_signup(
    db: DBSession = Depends(get_database),
    payload: AdminSignUpRequest = Body(...),
):
    """
    Create a new admin account.
    """
    await signup_admin(db=db, payload=payload)

    return {
        "success": True,
        "message": "Admin created successfully",
    }


@router.post("/login")
async def admin_login(
    response: Response,
    request: Request,
    db: DBSession = Depends(get_database),
    payload: AdminLoginRequest = Body(...),
):
    """
    Authenticate admin and set auth cookies.
    """
    # Extract client IP safely
    ip_address = request.client.host if request.client else None

    # Authenticate admin
    tokens = await login_admin(
        db=db,
        payload=payload,
        ip_address=ip_address,
    )

    access_token = tokens.access_token
    refresh_token = tokens.refresh_token

    # Set access token cookie (short-lived)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )

    # Set refresh token cookie (long-lived)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )

    return {
        "success": True,
        "message": "Login successful",
    }


@router.post("/refresh_access_token")
async def admin_refresh_access_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_database),
):
    # get the refresh token from the cookie

    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return {
            "success": False,
            "message": "Refresh token missing",
        }
    # pass the refresh token token the service function
    tokens = await refresh_admin_token(db=db, refresh_token=refresh_token)

    # set the new access token in the cookie
    access_token = tokens["access_token"]

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    # also sent the refresh token in the response
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )

    return {
        "success": True,
        "message": "Access token refreshed successfully",
    }
