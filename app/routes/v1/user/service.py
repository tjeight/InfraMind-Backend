from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.session import get_database
from app.dependencies.auth import get_current_user
from app.schemas.services.service import (
    ServiceDeleteRequest,
    ServiceRegisterRequest,
    ServiceUpdateRequest,
)
from app.services.services.services import (
    delete_service,
    get_services_by_company,
    register_service,
    update_service,
)
from app.types.auth import TypeUUID, UserData

# Configure the router
router = APIRouter(prefix="/v1/user/service", tags=["User Services"])


# Route to register a new service
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def service_register(
    _auth: UserData = Depends(get_current_user),
    payload: ServiceRegisterRequest = Body(...),
    db: AsyncSession = Depends(get_database),
):
    """Service registration route handler"""

    new_service = await register_service(db=db, payload=payload)

    return {"service_id": str(new_service.service_id)}


# Route to get services by company
@router.get("/company", status_code=status.HTTP_200_OK)
async def service_get_by_company(
    _auth: UserData = Depends(get_current_user),
    company_id: TypeUUID = Query(..., description="Company ID to filter services"),
    db: AsyncSession = Depends(get_database),
):
    """Get services by company route handler"""

    services = await get_services_by_company(db=db, company_id=company_id)

    return {"services": services}


# Route to update service details
@router.put("/update", status_code=status.HTTP_200_OK)
async def service_update(
    _auth: UserData = Depends(get_current_user),
    payload: ServiceUpdateRequest = Body(...),
    db: AsyncSession = Depends(get_database),
):
    """Service update route handler"""

    updated_service = await update_service(
        db=db, service_id=payload.service_id, payload=payload
    )

    return {"service_id": str(updated_service.service_id)}


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def service_delete(
    _auth: UserData = Depends(get_current_user),
    payload: ServiceDeleteRequest = Body(...),
    db: AsyncSession = Depends(get_database),
):
    """Service delete route handler"""

    _result = await delete_service(db=db, payload=payload)

    return {"message": "Service deleted successfully"}
