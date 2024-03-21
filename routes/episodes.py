from fastapi import APIRouter
from data.cache import cache

router = APIRouter()


@router.get("filter")
async def filter_episodes():
    """
    Filter episodes by criteria
    """
    return {"message": "Filter episodes by criteria"}


@router.get("/character-count-sorted")
async def character_count_sorted():
    """
    All episodes sorted by most characters
    """
    return {"message": "All episodes sorted by most characters"}


@router.get("/duration-sorted")
async def duration_sorted():
    """
    All episodes sorted by duration
    """
    return {"message": "All episodes sorted by duration"}


@router.get("/air-date-sorted")
async def air_date_sorted():
    """
    All episodes sorted by air date
    """
    return {"message": "All episodes sorted by air date"}
