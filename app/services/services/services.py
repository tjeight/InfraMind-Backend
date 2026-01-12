from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.services.services import Service
from app.schemas.services.service import (
    ServiceDeleteRequest,
    ServiceRegisterRequest,
    ServiceUpdateRequest,
)
from app.types.auth import TypeUUID


# Service to handle service registration
async def register_service(db: AsyncSession, payload: ServiceRegisterRequest):
    company_id = payload.company_id
    name = payload.name
    base_url = payload.base_url
    scope_path = payload.scope_path
    environment = payload.environment

    # Logic to register the service in the database
    new_service = Service(
        company_id=company_id,
        name=name,
        base_url=base_url,
        scope_path=scope_path,
        environment=environment,
    )
    db.add(new_service)
    await db.commit()
    await db.refresh(new_service)
    return new_service


# Function to get the user register
async def get_services_by_company(db: AsyncSession, company_id: TypeUUID):
    result = await db.execute(select(Service).where(Service.company_id == company_id))
    services = result.scalars().all()
    return services


# Service to update the service details
async def update_service(
    db: AsyncSession, service_id: TypeUUID, payload: ServiceUpdateRequest
):
    result = await db.execute(select(Service).where(Service.service_id == service_id))
    service = result.scalar_one_or_none()

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )
    if payload.name is not None:
        service.name = payload.name
    if payload.base_url is not None:
        service.base_url = payload.base_url
    if payload.scope_path is not None:
        service.scope_path = payload.scope_path
    if payload.environment is not None:
        service.environment = payload.environment
    if payload.is_active is not None:
        service.is_active = payload.is_active

    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service


# Service to delete a service
async def delete_service(db: AsyncSession, payload: ServiceDeleteRequest):
    service_id = payload.service_id
    company_id = payload.company_id

    result = await db.execute(
        select(Service).where(
            Service.service_id == service_id,
            Service.company_id == company_id,
        )
    )
    service = result.scalar_one_or_none()

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found"
        )

    await db.delete(service)
    await db.commit()
    return {"detail": "Service deleted successfully"}
