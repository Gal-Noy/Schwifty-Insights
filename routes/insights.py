from typing import Annotated

from fastapi import APIRouter, Depends
import data.analysis as analysis
from utils import pagination
from utils.auth import oauth2_scheme

router = APIRouter()


@router.get("/characters-relationships")
async def characters_relationships(token: Annotated[str, Depends(oauth2_scheme)],
                                   page: int = 1):
    """
    Estimate relationships between characters according to their appearances in the whole series.
    :param token:
    :param page:
    :return: List of tuples with the relationship level and the characters that have that relationship.
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
    character_relationships_groups = analysis.characters_relationships(len(relationships_levels))

    # Smaller size = closer relationship
    sorted_by_length = sorted(character_relationships_groups.items(), key=lambda x: len(x[1]))

    # Label relationships with levels
    relationships_labeled = []
    for i, (cluster_id, items) in enumerate(sorted_by_length):
        relationships_labeled.append((relationships_levels[i], items))

    return pagination.paginate_list_of_tuples(relationships_labeled, page)


@router.get("/dimension-species-diversity")
async def dimension_species_diversity(token: Annotated[str, Depends(oauth2_scheme)],
                                      page: int = 1):
    """
    List dimensions and the number of species that appear in each one.
    Are there dimensions with higher species diversity?
    :param token:
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

    return pagination.paginate_list_of_tuples(diversity_labeled, page)


@router.get("/dangerous-locations")
async def dangerous_locations(token: Annotated[str, Depends(oauth2_scheme)],
                              page: int = 1):
    """
    Analyze the correlation between a character's location and their status.
    Are there locations with higher mortality rates?
    :param token:
    :param page:
    :return: List of locations and their mortality rates
    """
    danger_threshold = 0.75  # 75% of characters in a location are dead or unknown
    result = analysis.dangerous_locations(danger_threshold)
    sorted_by_danger = sorted(result, key=lambda x: x[1])
    return pagination.paginate_list([(label, f"Mortality Rate: {round(_ * 100, 2)}%") for label, _ in sorted_by_danger], page)


@router.get("/species-survival")
async def species_survival(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Analyze the correlation between a character's species and their status.
    Are there species that are more likely to survive?
    :param token:
    :return: List of species and their survival rates
    """
    species_survival_rates = analysis.species_survival()
    sorted_by_survival_rate = sorted(species_survival_rates.items(), key=lambda x: x[1], reverse=True)
    return [{"species": species, "survival_rate": f"{round(survival_rate * 100, 2)}%"}
            for species, survival_rate in sorted_by_survival_rate]


@router.get("/native-species")
async def native_species(token: Annotated[str, Depends(oauth2_scheme)],
                         page: int = 1):
    """
    Estimate the native species of each location.
    :param token:
    :param page:
    :return: List of locations and their native species
    """
    return pagination.paginate_list(analysis.native_species(), page)


@router.get("/gender-by-location-type")
async def gender_by_location_type(token: Annotated[str, Depends(oauth2_scheme)],
                                  page: int = 1):
    """
    Analyze the correlation between a character's gender and their location type.
    :param token:
    :param page:
    :return: List of locations types and their most common gender
    """
    result = analysis.gender_by_location_type()

    re_ordered = {}
    for k, v in result:
        re_ordered.setdefault(v, []).append(k)

    result = [(v, keys) for v, keys in re_ordered.items()]
    return pagination.paginate_list(result, page)


@router.get("/interdimensional-travelers")
async def interdimensional_travelers(token: Annotated[str, Depends(oauth2_scheme)],
                                     page: int = 1):
    """
    Report characters who travel between dimensions.
    :param page:
    :param token:
    :return: List of characters who travel between dimensions
    """
    interdimensional_travelers_list = analysis.interdimensional_travelers()
    labeled_list = [(character, f"Dimensions: {', '.join(dimensions)}")
                    for character, dimensions in interdimensional_travelers_list]
    return pagination.paginate_list(labeled_list, page)


@router.get("/frequent-travelers")
async def frequent_travelers(token: Annotated[str, Depends(oauth2_scheme)],
                             page: int = 1):
    """
    Report characters which change locations frequently.
    :param page:
    :param token:
    :return: List of characters who change locations frequently
    """
    return pagination.paginate_list(analysis.frequent_travelers(), page)


@router.get("/main-characters")
async def main_characters(token: Annotated[str, Depends(oauth2_scheme)],
                          page: int = 1):
    """
        Report the main characters of the series.
        :param page:
        :param token:
        :return: List of main characters
        """
    threshold = 0.5
    return pagination.paginate_list(analysis.main_characters(threshold), page)
