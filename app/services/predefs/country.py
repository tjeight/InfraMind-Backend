from fastapi.exceptions import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from app.models.predefs.country import Country
from app.schemas.predefs.country import (
    CountryDeleteRequest,
    CountryListRequest,
    CountryUpdateRequest,
)
from app.utils.generators import get_uuid


# Admin Function to  add the countries
async def countries_add(db: AsyncSession, payload: CountryListRequest):
    """Function to add predefined countries to the database"""
    try:
        country_objects = [
            Country(
                country_id=get_uuid(),
                country_name=country.country_name,
                country_code=country.country_code,
            )
            for country in payload.countries
        ]

        db.add_all(country_objects)
        await db.commit()
        return country_objects
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Function to get all predefined countries
async def get_all_countries(db: AsyncSession):
    """Function to get all predefined countries from the database"""
    # Get all the countries
    result = await db.execute(select(Country).order_by(Country.country_name))
    countries = result.scalars().all()
    return countries


# Function to update the country information
async def update_country(db: AsyncSession, payload: CountryUpdateRequest):
    """Function to update the country information"""
    # Get the country
    query = await db.execute(
        select(Country).where(Country.country_id == payload.country_id)
    )
    country = query.scalars().first()

    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Country not found",
        )
    # Update the country information
    country.country_name = payload.country_name
    country.country_code = payload.country_code

    #  Commit the changes
    await db.commit()
    await db.refresh(country)
    return country


# Function to delete the country ids
async def delete_country(db: AsyncSession, payload: CountryDeleteRequest):
    """Function to delete the countries"""
    try:
        #  delete the countries
        await db.execute(
            delete(Country).where(Country.country_id.in_(payload.country_ids))
        )

        # commit the changes
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
