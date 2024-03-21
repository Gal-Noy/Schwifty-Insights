from fastapi import APIRouter
from data.cache import cache

router = APIRouter()


@router.get("/filter")
async def filter_characters():
    """
    Filter characters by criteria
    """
    return {"message": "Filter characters by criteria"}


@router.get("/appearances-sorted")
async def appearances_sorted():
    """
    All characters sorted by most appearances in episodes
    """
    return {"message": "All characters sorted by most appearances in episodes"}


@router.get("/status-sorted")
async def status_sorted():
    """
    All characters sorted by status
    """
    return {"message": "All characters sorted by status"}


@router.get("/most-common-species")
async def most_common_species():
    """
    Most common species
    """
    return {"message": "Most common species"}










