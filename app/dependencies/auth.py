import jwt
from fastapi import HTTPException, Request, status

from app.configs.settings import settings
from app.schemas.auth.admin import AdminData
from app.schemas.auth.user import UserData


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


# Dependency to authenticate the user
async def get_current_user(
    request: Request,
) -> UserData:
    """Dependency to get the current authenticated user from the access token."""

    try:
        # Get the token from the request cookies
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

        # Extract user_id from the payload
        user_id: str | None = payload.get("user_id")

        # Validate user_id presence
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )

        return UserData(user_id=user_id)

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
