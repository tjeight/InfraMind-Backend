from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.predefs.predef_role_model import PredefRegistrationRole
from app.schemas.predefs.predef_role_schema import (
    PredefRegistrationRolePostRequestSchema,
)


async def predef_registration_role_post(
    db: AsyncSession,
    payload: PredefRegistrationRolePostRequestSchema,
):
    # 1. Fetch existing roles
    result = await db.execute(
        select(PredefRegistrationRole).where(
            PredefRegistrationRole.role_name.in_(payload.role_names)
        )
    )
    existing_roles = result.scalars().all()

    # 2. Extract existing role names
    existing_role_names = {role.role_name for role in existing_roles}

    # 3. Find missing roles
    new_role_names = [
        role_name
        for role_name in payload.role_names
        if role_name not in existing_role_names
    ]

    # 4. Create ORM objects for missing roles
    new_roles = [
        PredefRegistrationRole(role_name=role_name) for role_name in new_role_names
    ]

    # 5. Persist new roles
    if new_roles:
        db.add_all(new_roles)
        await db.commit()
        for role in new_roles:
            await db.refresh(role)

    # 6. Return combined result
    return {
        "created_roles": new_roles,
        "existing_roles": existing_roles,
    }
