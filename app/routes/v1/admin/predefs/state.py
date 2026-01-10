from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.session import get_database
from app.dependencies.auth import get_current_admin
from app.schemas.auth.admin import AdminData
from app.schemas.predefs.state import (
    StateDeleteRequest,
    StateListRequest,
    StateUpdateRequest,
)
from app.services.predefs.state import (
    delete_states,
    get_all_states,
    states_add,
    update_state,
)

# Configure the api router
router = APIRouter(prefix="/predefs/states", tags=["Admin Predefined States"])


@router.post("/state")
async def state_post(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
    payload: StateListRequest = Body(...),
):
    """Router Function to add predefined states to the database"""

    # Add the states
    _states = await states_add(db=db, payload=payload)

    return {
        "success": True,
        "message": "States added successfully",
    }


@router.get("/states")
async def states_get(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
):
    """Router Function to get all predefined states from the database"""

    # Get all the states
    states = await get_all_states(db=db)

    # Create proper states response
    states = [
        {
            "state_id": state.state_id,
            "state_name": state.state_name,
            "country_id": state.country_id,
        }
        for state in states
    ]
    return {
        "success": True,
        "states": states,
    }


@router.put("/state")
async def state_put(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
    payload: StateUpdateRequest = Body(...),
):
    """Router Function to update the state information"""

    # Update the state information
    await update_state(db=db, payload=payload)

    return {
        "success": True,
        "message": "State updated successfully",
    }


@router.delete("/state")
async def states_delete(
    db: AsyncSession = Depends(get_database),
    _auth: AdminData = Depends(get_current_admin),
    payload: StateDeleteRequest = Body(...),
):
    """Router Function to delete predefined states"""

    # Delete the states
    await delete_states(db=db, payload=payload)

    return {
        "success": True,
        "message": "States deleted successfully",
    }
