from fastapi import APIRouter, Request, Response, status

from app.configs import settings
from app.configs.settings import settings
from app.schemas.auth.admin import AdminLoginRequest, AdminSignUpRequest
from app.types.db import DBSession
from app.services.auth.admin import login_admin, signup_admin

# Configure router
router = APIRouter(prefix="/admin", tags=["Admin Auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def admin_signup(
    db: DBSession,
    payload: AdminSignUpRequest,
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
    db: DBSession,
    payload: AdminLoginRequest,
    request: Request,
    response: Response,
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

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

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
