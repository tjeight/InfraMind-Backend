from fastapi.exceptions import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from app.models.predefs.city import City
from app.schemas.predefs.city import (
    CityDeleteRequest,
    CityListRequest,
    CityUpdateRequest,
)
from app.utils.generators import get_uuid


# Function to add predefined cities
async def cities_add(db: AsyncSession, payload: CityListRequest):
    """Function to add predefined cities to the database"""
    try:
        city_objects = [
            City(
                city_id=get_uuid(),
                city_name=city.city_name,
                state_id=city.state_id,
            )
            for city in payload.cities
        ]

        db.add_all(city_objects)
        await db.commit()
        return city_objects
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Function to get all predefined cities
async def get_all_cities(db: AsyncSession):
    """Function to get all predefined cities from the database"""
    try:
        # Get all the cities
        result = await db.execute(select(City).order_by(City.city_name))
        cities = result.scalars().all()
        return cities
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Function to update the city information
async def update_city(db: AsyncSession, payload: CityUpdateRequest):
    """Function to update the city information"""
    try:
        # Get the city
        query = await db.execute(select(City).where(City.city_id == payload.city_id))
        city = query.scalars().first()

        if not city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )
        # Update the city information
        city.city_name = payload.city_name or city.city_name
        city.state_id = payload.state_id or city.state_id

        db.add(city)
        await db.commit()
        return city
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Function to delete predefined cities
async def delete_cities(db: AsyncSession, payload: CityDeleteRequest):
    """Function to delete the cities"""
    try:
        #  delete the cities
        await db.execute(delete(City).where(City.city_id.in_(payload.city_ids)))

        # commit the changes
        await db.commit()
        return
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
