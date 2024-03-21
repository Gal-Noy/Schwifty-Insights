from fastapi import APIRouter
from data.cache import cache

router = APIRouter()


@router.get("/estimate-relationships")
async def estimate_relationships():
    """
    Estimate relationships between characters according to their appearances in the whole series.
    """
    return {"message": "Estimate relationships"}


@router.get("/estimate-relationships-per-season")
async def estimate_relationships_per_season():
    """
    Estimate relationships between characters according to their appearances in each season.
    """
    return {"message": "Estimate relationships per season"}


@router.get("/species-status-correlation")
async def species_status_correlation():
    """
    Analyze the correlation between a character's species and their status (dead/alive/unknown).
    Are there species with higher mortality rates?
    """
    return {"message": "Species and status correlation"}


@router.get("/species-location-correlation")
async def species_location_correlation():
    """
    Analyze the correlation between a character's species and their location.
    Are there species that are more likely to be in a specific location?
    """
    return {"message": "Species by location"}


@router.get("/location-status-correlation")
async def location_status_correlation():
    """
    Analyze the correlation between a character's location and their status.
    Are there locations with higher mortality rates?
    """
    return {"message": "Location and status correlation"}


@router.get("/location-species-diversity")
async def location_species_diversity():
    """
    List locations and the number of species that appear in each one.
    Are there locations with higher species diversity?
    """
    return {"message": "Location and species diversity"}


@router.get("/status-appearances-correlation")
async def status_appearances_correlation():
    """
    Estimate correlation between character status and number of episodes they appear in.
    """
    return {"message": "Status correlation between character status and number of episodes they appear in"}


@router.get("/frequent-location-changes")
async def frequent_location_changes():
    """
    Report characters which change locations frequently.
    """
    return {"message": "Characters which change locations frequently"}
