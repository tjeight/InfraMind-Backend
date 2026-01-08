from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.auth.admin_session import AdminSession
from app.schemas.auth.admin import AdminLoginRequest, AdminSignUpRequest, TokenResponse
from app.utils.auth import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.auth.admin import Admin
from app.configs.settings import settings
from app.utils.generators import get_current_datetime


async def signup_admin(db: AsyncSession, payload: AdminSignUpRequest):
    """
    Create a new admin account.

    Steps:
    1. Hash the password
    2. Persist admin record
    3. Return created admin
    """
    try:
        # Extract payload data
        name = payload.name
        password = payload.password
        email = payload.email

        # Securely hash the password before storage
        password_hash = hash_password(password=password)

        # Create admin entity
        admin = Admin(
            name=name,
            password_hash=password_hash,
            email=email,
        )

        # Persist admin
        db.add(admin)
        await db.commit()
        await db.refresh(admin)

        return admin

    except Exception:
        # Generic failure during signup
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create admin account",
        )


async def login_admin(
    db: AsyncSession,
    payload: AdminLoginRequest,
    ip_address: str | None,
) -> TokenResponse:
    """
    Authenticate admin and issue tokens.

    Flow:
    1. Validate credentials
    2. Create access token
    3. Create session
    4. Issue refresh token bound to session
    """
    try:
        # Fetch admin by email
        result = await db.execute(select(Admin).where(Admin.email == payload.email))
        admin = result.scalar_one_or_none()

        if not admin:
            # Avoid leaking whether email exists
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        # Verify password
        if not verify_password(payload.password, admin.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        # Prepare access token payload
        access_token_payload = {
            "admin_id": str(admin.admin_id),
        }

        # Generate short-lived access token
        access_token = create_access_token(access_token_payload)

        # Create a new session (refresh token will be attached later)
        session = AdminSession(
            admin_id=str(admin.admin_id),
            ip_address=ip_address,
        )

        # Persist session to obtain session ID
        db.add(session)
        await db.flush()

        # Prepare refresh token payload bound to this session
        refresh_token_payload = {
            "admin_id": str(admin.admin_id),
            "session_id": str(session.admin_session_id),
        }

        # Generate refresh token
        refresh_token = create_refresh_token(refresh_token_payload)

        # Update session with refresh token and expiry
        session.refresh_token = refresh_token
        session.expires_at = get_current_datetime() + settings.refresh_token_expire

        # Commit all changes atomically
        await db.commit()

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    except HTTPException:
        # Re-raise expected authentication errors
        raise

    except Exception:
        import traceback

        traceback.print_exc()
        # Catch-all for unexpected failures
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed due to internal error",
        )


# Function to refresh admin access tokens
async def refresh_admin_token(db: AsyncSession, refresh_token: str) -> dict[str, str]:
    """
    Refresh admin access token using a valid refresh token.

    Steps:
    1. Validate refresh token and session
    2. Issue new access token
    3. Optionally issue new refresh token
    """
    try:
        # Fetch session by refresh token
        result = await db.execute(
            select(AdminSession).where(AdminSession.refresh_token == refresh_token)
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

        # Get the admin_id from the session
        admin_id = session.admin_id

        # Prepare new access token payload
        access_token_payload = {
            "admin_id": str(admin_id),
        }

        # Generate new access token
        access_token = create_access_token(access_token_payload)

        return {
            "access_token": access_token,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh token",
        )


# Function to handle the admin forgot password
# TODO: Implement the flow after wards with resend
# async def forgot_password_admin(db:AsyncSession,)
