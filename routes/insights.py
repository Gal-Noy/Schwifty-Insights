from fastapi import APIRouter
import data.analysis as analysis
import utils

router = APIRouter()


@router.get("/estimate-relationships")
async def estimate_relationships(page: int = 1):
    """
    Estimate relationships between characters according to their appearances in the whole series.
    :param page:
    :return:  List of tuples with the relationship level and the characters that have that relationship.
    """

    relationships_levels = {
        0: "Very Close Relationship",
        1: "Close Relationship",
        2: "Strong Relationship",
        3: "Good Relationship",
        4: "Normal Relationship",
        5: "Fair Relationship",
        6: "Weak Relationship",
        7: "Poor Relationship",
        8: "Very Poor Relationship",
        9: "Farthest Relationship"
    }

    character_relationships_groups = analysis.estimate_relationships(len(relationships_levels))

    # Smaller size = closer relationship
    sorted_by_length = sorted(character_relationships_groups.items(), key=lambda x: len(x[1]))

    # Label relationships with levels
    relationships_labeled = []
    for i, (cluster_id, items) in enumerate(sorted_by_length):
        relationships_labeled.append((relationships_levels[i], items))

    return utils.paginate_list_of_tuples(relationships_labeled, page)


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
