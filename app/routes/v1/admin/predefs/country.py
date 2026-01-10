from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.session import get_database
from app.dependencies.auth import get_current_admin
from app.schemas.auth.admin import AdminData
from app.schemas.predefs.country import (
    CountryDeleteRequest,
    CountryListRequest,
    CountryUpdateRequest,
)
from app.services.predefs.country import (
    countries_add,
    delete_country,
    get_all_countries,
    update_country,
)

# Configure the api router
router = APIRouter(prefix="/predefs/countries", tags=["Admin Predefined Countries"])


@router.post("/country")
async def country_post(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
    payload: CountryListRequest = Body(...),
):
    """Router Function  to add predefined countries to the database"""

    #  Add the countries
    _countries = await countries_add(db=db, payload=payload)

    return {
        "success": True,
        "message": "Countries added successfully",
    }


@router.get("/countries")
async def countries_get(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
):
    """Router Function to get all predefined countries from the database"""

    # Get all the countries
    countries = await get_all_countries(db=db)

    # Create proper countries response
    countries = [
        {
            "country_id": country.country_id,
            "country_name": country.country_name,
            "country_code": country.country_code,
        }
        for country in countries
    ]
    return {
        "success": True,
        "message": "Countries fetched successfully",
        "data": countries,
    }


@router.put("/country")
async def country_put(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
    payload: CountryUpdateRequest = Body(...),
):
    """Router Function to update the country information"""

    # Update the country information
    await update_country(db=db, payload=payload)

    return {
        "success": True,
        "message": "Country updated successfully",
    }


@router.delete("/countries")
async def countries_delete(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
    payload: CountryDeleteRequest = Body(...),
):
    """Router Function to delete the countries"""

    # Delete the countries
    await delete_country(db=db, payload=payload)

    return {
        "success": True,
        "message": "Countries deleted successfully",
    }
