from pydantic import BaseModel
from app.types.auth import TypeUUID


# Schema for a single state item
class StateItem(BaseModel):
    state_name: str
    country_id: TypeUUID


# Schema for list of states
class StateListRequest(BaseModel):
    states: list[StateItem]


# Schema to update the state response
class StateUpdateRequest(BaseModel):
    state_id: TypeUUID
    state_name: str
    country_id: TypeUUID


# Schema for delete the states
class StateDeleteRequest(BaseModel):
    state_ids: list[TypeUUID]
