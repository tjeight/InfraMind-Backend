import jwt
from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.settings import settings
from app.schemas.auth.admin import AdminData


#  Dependency to authenticate the admin
async def get_current_admin(
    request: Request,
) -> AdminData:
    """Dependency to get the current authenticated admin from the access token."""

    try:
        #  Get the token from the request cookies
        token: str | None = request.cookies.get("access_token")

        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication credentials were not provided",
            )

        # Decode the JWT token
        payload: dict = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        # Extract admin_id from the payload
        admin_id: str | None = payload.get("admin_id")

        #  Validate admin_id presence
        if admin_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        admin = AdminData(admin_id=admin_id)

        return admin

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
