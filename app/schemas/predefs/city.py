from pydantic import BaseModel
from app.types.auth import TypeUUID


# Schema for a single city item
class CityItem(BaseModel):
    city_name: str
    state_id: TypeUUID


# Schema for list of cities
class CityListRequest(BaseModel):
    cities: list[CityItem]


# Schema to update the city response
class CityUpdateRequest(BaseModel):
    city_id: TypeUUID
    city_name: str | None = None
    state_id: TypeUUID | None = None


# Schema for delete the cities
class CityDeleteRequest(BaseModel):
    city_ids: list[TypeUUID]
