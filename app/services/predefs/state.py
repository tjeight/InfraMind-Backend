from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.predefs.state import State
from app.schemas.predefs.state import (
    StateDeleteRequest,
    StateListRequest,
    StateUpdateRequest,
)
from app.utils.generators import get_uuid


# Function to add predefined states
async def states_add(db: AsyncSession, payload: StateListRequest):
    """Function to add predefined states to the database"""
    try:
        state_objects = [
            State(
                state_id=get_uuid(),
                state_name=state.state_name,
                country_id=state.country_id,
            )
            for state in payload.states
        ]

        db.add_all(state_objects)
        await db.commit()
        return state_objects
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


#  Function to get all predefined states
async def get_all_states(db: AsyncSession):
    """Function to get all predefined states from the database"""
    # Get all the states
    result = await db.execute(select(State).order_by(State.state_name))
    states = result.scalars().all()
    return states


# Function to update the state information
async def update_state(db: AsyncSession, payload: StateUpdateRequest):
    """Function to update the state information"""
    # Get the state
    query = await db.execute(select(State).where(State.state_id == payload.state_id))
    state = query.scalars().first()

    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="State not found",
        )

    # Update the state information
    state.state_name = payload.state_name
    state.country_id = payload.country_id

    db.add(state)
    await db.commit()
    await db.refresh(state)
    return state


# Function to delete a predefined states
async def delete_states(db: AsyncSession, payload: StateDeleteRequest):
    """Function to delete predefined states from the database"""
    try:
        # Delete the states
        await db.execute(delete(State).where(State.state_id.in_(payload.state_ids)))
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
