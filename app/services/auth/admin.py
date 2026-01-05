from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth.admin import AdminSignUpRequest
from app.utils.auth import hash_password
from app.models.auth.admin import Admin


async def signup_admin(db: AsyncSession, payload: AdminSignUpRequest):
    try:
        # get all the details
        name = payload.name
        password = payload.password
        email = payload.email

        # hash the password
        password_hash = hash_password(password=password)

        # create an Admin
        admin = Admin(name=name, password_hash=password_hash, email=email)

        # add to the db
        db.add(admin)

        # commit the changes
        await db.commit()

        # refresh the db
        await db.refresh(admin)

        return admin

    except Exception as e:
        raise e
