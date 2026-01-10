from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company.company import Company
from app.schemas.company.company import (
    CompanyDeleteRequest,
    CompanyRegisterRequest,
    CompanyUpdateRequest,
)
from app.types.auth import TypeUUID, UserData


#  Function to add the company
async def create_company(
    db: AsyncSession, payload: CompanyRegisterRequest, auth: UserData
):
    try:
        #  get all the details from the payload
        company_name = payload.company_name
        company_slug = payload.company_slug
        company_website = payload.company_website
        user_id = auth.user_id

        #  Create the company object
        new_company = Company(
            company_name=company_name,
            company_slug=company_slug,
            company_website=company_website,
            user_id=user_id,
        )

        #  Add the company to the database
        db.add(new_company)
        await db.commit()
        await db.refresh(new_company)
        return new_company

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Function to get the companies by user id
async def get_companies_by_user_id(db: AsyncSession, auth: UserData):
    try:
        user_id = auth.user_id
        result = await db.execute(select(Company).where(Company.user_id == user_id))
        companies = result.scalars().all()

        if not companies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No companies found for the user",
            )
        return companies

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Function to get company by company id
async def get_company_by_id(db: AsyncSession, company_id: TypeUUID, auth: UserData):
    try:
        user_id = auth.user_id
        result = await db.execute(
            select(Company).where(
                Company.company_id == company_id, Company.user_id == user_id
            )
        )
        company = result.scalar_one_or_none()

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )

        return company
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Function to update the company information
async def update_company(
    db: AsyncSession, payload: CompanyUpdateRequest, auth: UserData
):
    try:
        # get the company
        company = await get_company_by_id(db, payload.company_id, auth)

        # update the company details
        if payload.company_name is not None:
            company.company_name = payload.company_name
        if payload.company_slug is not None:
            company.company_slug = payload.company_slug
        if payload.company_website is not None:
            company.company_website = payload.company_website
        if payload.is_active is not None:
            company.is_active = payload.is_active

        # commit the changes to the database
        db.add(company)
        await db.commit()
        await db.refresh(company)
        return company

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Function to delete the companies
async def delete_company(
    db: AsyncSession, payload: CompanyDeleteRequest, auth: UserData
):
    try:
        await db.execute(
            delete(Company).where(
                Company.company_id.in_(payload.company_id),
                Company.user_id == auth.user_id,
            )
        )
        await db.commit()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
