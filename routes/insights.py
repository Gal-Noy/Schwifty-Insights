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

    # KMeans clustering
    character_relationships_groups = analysis.estimate_relationships(len(relationships_levels))

    # Smaller size = closer relationship
    sorted_by_length = sorted(character_relationships_groups.items(), key=lambda x: len(x[1]))

    # Label relationships with levels
    relationships_labeled = []
    for i, (cluster_id, items) in enumerate(sorted_by_length):
        relationships_labeled.append((relationships_levels[i], items))

    return utils.paginate_list_of_tuples(relationships_labeled, page)


@router.get("/species-survival")
async def species_survival():
    """
    Analyze the correlation between a character's species and their status.
    Are there species that are more likely to survive?
    :return: List of species and their survival rates
    """
    species_survival_rates = analysis.species_survival()
    sorted_by_survival_rate = sorted(species_survival_rates.items(), key=lambda x: x[1], reverse=True)
    return [{"species": species, "survival_rate": f"{round(survival_rate * 100, 2)}%"}
            for species, survival_rate in sorted_by_survival_rate]


@router.get("/native-species")
async def native_species(page: int = 1):
    """
    Estimate the native species of each location.
    :param page:
    :return:  List of locations and their native species
    """
    return utils.paginate_list(analysis.native_species(), page)


@router.get("/dangerous-locations")
async def dangerous_locations(page: int = 1):
    """
    Analyze the correlation between a character's location and their status.
    Are there locations with higher mortality rates?
    :param page:
    :return: List of locations and their mortality rates
    """
    danger_threshold = 0.75  # 75% of characters in a location are dead or unknown
    result = analysis.dangerous_locations(danger_threshold)
    sorted_by_danger = sorted(result, key=lambda x: x[1], reverse=True)
    return utils.paginate_list([(label, f"Mortality Rate: {_ * 100}%") for label, _ in sorted_by_danger], page)


@router.get("/dimension-species-diversity")
async def dimension_species_diversity(page: int = 1):
    """
    List dimensions and the number of species that appear in each one.
    Are there dimensions with higher species diversity?
    :param page:
    :return: List of dimensions and their species diversity
    """
    diversity_level = {
        0: "Very High Diversity",
        1: "High Diversity",
        2: "Medium Diversity",
        3: "Low Diversity",
        4: "Very Low Diversity"
    }

    # KMeans clustering
    dimension_species_diversity_groups = analysis.dimension_species_diversity(len(diversity_level))

    # Label diversity levels
    diversity_labeled = []
    for i, (cluster_id, items) in enumerate(dimension_species_diversity_groups):
        diversity_labeled.append((diversity_level[i], items))

    return utils.paginate_list_of_tuples(diversity_labeled, page)


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
