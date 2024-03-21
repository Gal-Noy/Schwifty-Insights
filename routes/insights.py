from fastapi import APIRouter

router = APIRouter()


@router.get("/episodes-duration-character-count")
async def episodes_duration_character_count():
    """
    Episodes duration and character count
    """
    return {"message": "Episodes duration and character count"}


@router.get("/dimension-most-frequent-species")
async def dimension_most_frequent_species():
    """
    Dimension and most frequent species
    """
    return {"message": "Dimension and most frequent species"}


@router.get("/status-appearances-correlation")
async def status_appearances_correlation():
    """
    Status correlation between character status and number of episodes they appear in
    """
    return {"message": "Status correlation between character status and number of episodes they appear in"}


@router.get("/frequent-location-changes")
async def frequent_location_changes():
    """
    Characters which change locations frequently
    """
    return {"message": "Characters which change locations frequently"}