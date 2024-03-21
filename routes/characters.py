from fastapi import APIRouter
from data.client import fetch_characters
from data.cache import cache


def get_characters():
    cached_characters = cache.get("characters")
    if cached_characters:
        return cached_characters
    else:
        characters = fetch_characters()
        cache["characters"] = characters
        return characters


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










