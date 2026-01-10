from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.session import get_database
from app.configs.settings import settings
from app.schemas.auth.user import UserLoginRequest, UserSignUpRequest
from app.services.auth.user import refresh_user_token, user_login, user_signup

# Configure the router
router = APIRouter(prefix="/v1/user/auth", tags=["User Authentication"])


# Function for user signup
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup_user(
    payload: UserSignUpRequest = Body(...),
    db: AsyncSession = Depends(get_database),
):
    """User signup route handler"""

    new_user = await user_signup(db=db, payload=payload)

    return {"user_id": str(new_user.user_id)}


# Route for the user login
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    request: Request,
    response: Response,
    payload: UserLoginRequest = Body(...),
    db: AsyncSession = Depends(get_database),
):
    """User login route handler"""
    tokens = await user_login(db=db, payload=payload)

    # create secure cookies for access and refresh tokens
    response.set_cookie(
        key="access_token",
        value=tokens.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        secure=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # 7 days
        samesite="lax",
    )
    return {"message": "Login successful"}


# Router to refresh the access token
@router.post("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_access_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_database),
):
    """Route to refresh the access token using the refresh token cookie"""
    refresh_token: str | None = request.cookies.get("refresh_token")

    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not provided",
        )

    try:
        #   pass the refresh
        access_token = await refresh_user_token(db=db, refresh_token=refresh_token)

        # set the new access token in the cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # 7 days
            samesite="lax",
        )

        return {"message": "Access token refreshed successfully"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh access token",
        )
