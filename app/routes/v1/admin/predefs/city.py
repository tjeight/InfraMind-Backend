from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.session import get_database
from app.dependencies.auth import get_current_admin
from app.schemas.auth.admin import AdminData
from app.schemas.predefs.city import (
    CityDeleteRequest,
    CityListRequest,
    CityUpdateRequest,
)
from app.services.predefs.city import (
    delete_cities,
    get_all_cities,
    cities_add,
    update_city,
)

# Configure the api router
router = APIRouter(prefix="/predefs/cities", tags=["Admin Predefined Cities"])


@router.post("/city")
async def city_post(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
    payload: CityListRequest = Body(...),
):
    """Router Function to add predefined cities to the database"""

    # Add the cities
    _cities = await cities_add(db=db, payload=payload)

    return {
        "success": True,
        "message": "Cities added successfully",
    }


@router.get("/cities")
async def cities_get(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
):
    """Router Function to get all predefined cities from the database"""

    # Get all the cities
    cities = await get_all_cities(db=db)

    # Create proper cities response
    cities = [
        {
            "city_id": city.city_id,
            "city_name": city.city_name,
            "state_id": city.state_id,
        }
        for city in cities
    ]
    return {
        "success": True,
        "cities": cities,
    }


@router.put("/city")
async def city_put(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
    payload: CityUpdateRequest = Body(...),
):
    """Router Function to update the city information"""

    # Update the city information
    _city = await update_city(db=db, payload=payload)

    return {
        "success": True,
        "message": "City updated successfully",
    }


@router.delete("/city")
async def city_delete(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
    payload: CityDeleteRequest = Body(...),
):
    """Router Function to delete predefined cities from the database"""

    # Delete the cities
    await delete_cities(db=db, payload=payload)

    return {
        "success": True,
        "message": "Cities deleted successfully",
    }
