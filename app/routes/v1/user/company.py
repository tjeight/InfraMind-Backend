from fastapi import APIRouter, Body, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.session import get_database
from app.dependencies.auth import get_current_user
from app.schemas.company.company import (
    CompanyDeleteRequest,
    CompanyRegisterRequest,
    CompanyUpdateRequest,
)
from app.services.company.company import (
    create_company,
    delete_company,
    get_companies_by_user_id,
    get_company_by_id,
    update_company,
)
from app.types.auth import TypeUUID, UserData

# Configure the router
router = APIRouter(prefix="/v1/user/company", tags=["Company"])


# Route to create a new company
@router.post("/company", status_code=status.HTTP_201_CREATED)
async def register_company(
    payload: CompanyRegisterRequest = Body(...),
    db: AsyncSession = Depends(get_database),
    auth: UserData = Depends(get_current_user),
):
    _company = await create_company(db, payload, auth)

    return {
        "message": "Company created successfully",
    }


# Route to get all companies for the user
@router.get("/companies", status_code=status.HTTP_200_OK)
async def list_companies(
    db: AsyncSession = Depends(get_database),
    auth: UserData = Depends(get_current_user),
):
    try:
        companies = await get_companies_by_user_id(db, auth)

        companies = [
            {
                "company_id": str(company.company_id),
                "company_name": company.company_name,
                "company_website": company.company_website,
            }
            for company in companies
        ]

        return {"companies": companies}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Route to get a single company by ID
@router.get("/company", status_code=status.HTTP_200_OK)
async def get_company(
    company_id: TypeUUID,
    db: AsyncSession = Depends(get_database),
    auth: UserData = Depends(get_current_user),
):
    try:
        company = await get_company_by_id(db=db, company_id=company_id, auth=auth)

        # create the response
        response = {
            "company_id": company_id,
            "company_name": company.company_name,
            "company_website": company.company_website,
        }

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Route tpo update a company
async def update_company_details(
    payload: CompanyUpdateRequest = Body(...),
    db: AsyncSession = Depends(get_database),
    auth: UserData = Depends(get_current_user),
):
    try:
        await update_company(db, payload, auth)

        return {"message": "Company updated successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Router to delete a company
async def company_delete(
    db: AsyncSession = Depends(get_database),
    payload: CompanyDeleteRequest = Body(...),
    auth: UserData = Depends(get_current_user),
):
    try:
        await delete_company(db, payload, auth)

        return {"message": "Company deleted successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
