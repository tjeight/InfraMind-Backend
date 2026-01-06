from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.auth.admin_session import AdminSession
from app.schemas.auth.admin import AdminLoginRequest, AdminSignUpRequest
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
) -> dict[str, str]:
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
            "admin_id": admin.admin_id,
        }

        # Generate short-lived access token
        access_token = create_access_token(access_token_payload)

        # Create a new session (refresh token will be attached later)
        session = AdminSession(
            admin_id=admin.admin_id,
            ip_address=ip_address,
        )

        # Persist session to obtain session ID
        db.add(session)
        await db.flush()

        # Prepare refresh token payload bound to this session
        refresh_token_payload = {
            "admin_id": admin.admin_id,
            "session_id": session.admin_session_id,
        }

        # Generate refresh token
        refresh_token = create_refresh_token(refresh_token_payload)

        # Update session with refresh token and expiry
        session.refresh_token = refresh_token
        session.expires_at = get_current_datetime() + settings.refresh_token_expire

        # Commit all changes atomically
        await db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    except HTTPException:
        # Re-raise expected authentication errors
        raise

    except Exception:
        # Catch-all for unexpected failures
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed due to internal error",
        )
