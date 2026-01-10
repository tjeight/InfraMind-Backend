from pydantic import BaseModel

from app.types.auth import TypeUUID


# Schema for a single country item
class CountryItem(BaseModel):
    country_name: str
    country_code: str


# Schema for list of countries
class CountryListRequest(BaseModel):
    countries: list[CountryItem]


# Schema to update the country response
class CountryUpdateRequest(BaseModel):
    country_id: TypeUUID
    country_name: str
    country_code: str


# Schema for delete the countries
class CountryDeleteRequest(BaseModel):
    country_ids: list[TypeUUID]
