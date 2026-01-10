from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.settings import settings
from app.models.auth.user import User
from app.models.auth.user_session import UserSession
from app.schemas.auth.user import TokenResponse, UserLoginRequest, UserSignUpRequest
from app.utils.auth import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.utils.generators import get_current_datetime


#  Function to user signup
async def user_signup(db: AsyncSession, payload: UserSignUpRequest):
    """User signup function"""
    try:
        # get the email from payload
        email = payload.email

        # get the password and other details from payload
        password = payload.password
        first_name = payload.first_name
        last_name = payload.last_name

        country_id = payload.country_id
        state_id = payload.state_id
        city_id = payload.city_id

        #  hash the password
        hashed_password = hash_password(password)

        new_user = User(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            country_id=country_id,
            state_id=state_id,
            city_id=city_id,
            is_active=True,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


#  Function to user login
async def user_login(
    db: AsyncSession, payload: UserLoginRequest, ip_address: str | None = None
):
    """User login function"""
    try:
        # get the email
        email = payload.email

        # check if the user exists or not
        query = await db.execute(select(User).where(User.email == email))
        existing_user = query.scalar_one_or_none()

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        #  check the password
        if not verify_password(payload.password, existing_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        # create a new user session
        new_session = UserSession(user_id=existing_user.user_id, ip_address=ip_address)
        db.add(new_session)
        await db.flush()

        # create the payload for access token
        access_token_payload = {
            "user_id": str(existing_user.user_id),
            "session_id": str(new_session.user_session_id),
        }

        # create the access token
        access_token = create_access_token(access_token_payload)

        #  refresh token payload
        refresh_token_payload = {
            "user_id": str(existing_user.user_id),
            "session_id": str(new_session.user_session_id),
        }
        # create the refresh token
        refresh_token = create_refresh_token(refresh_token_payload)

        # add the refresh token to the session
        new_session.refresh_token = refresh_token
        new_session.is_active = True
        new_session.expires_at = get_current_datetime() + settings.refresh_token_expire

        # return the access token and refresh token
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Function to refresh user access tokens
async def refresh_user_token(db: AsyncSession, refresh_token: str) -> str:
    """
    Refresh user access token using a valid refresh token.

    Steps:
    1. Validate refresh token and session
    2. Issue new access token
    3. Optionally issue new refresh token
    """
    try:
        # Fetch session by refresh token
        result = await db.execute(
            select(UserSession).where(UserSession.refresh_token == refresh_token)
        )
        session = result.scalar_one_or_none()

        # Validate session existence and expiry
        if (
            not session
            or session.expires_at < get_current_datetime()
            or not session.is_active
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        # Create new access token payload
        access_token_payload = {
            "user_id": str(session.user_id),
            "session_id": str(session.user_session_id),
        }

        # Generate new access token
        access_token = create_access_token(access_token_payload)

        return access_token

    except HTTPException:
        # Re-raise expected authentication errors
        raise

    except Exception:
        # Catch-all for unexpected failures
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed due to internal error",
        )
