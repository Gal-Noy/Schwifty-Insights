from typing import Annotated

from fastapi import APIRouter, Depends

from utils.auth import oauth2_scheme
from utils.pagination import paginate_list
import data.cache as cache

router = APIRouter()


@router.get("/filter")
async def filter_locations(token: Annotated[str, Depends(oauth2_scheme)],
                           name: str = None,
                           type: str = None,
                           dimension: str = None,
                           at_least_residents: int = None,
                           page: int = 1):
    """
    Filter locations based on various attributes
    :param token:
    :param name:
    :param type:
    :param dimension:
    :param at_least_residents:
    :param page:
    :return: List of locations
    """
    locations = cache.get_all_locations()

    if name:
        locations = [location for location in locations if location["name"].lower().find(name) != -1]
    if type:
        locations = [location for location in locations if location["type"].lower().find(type) != -1]
    if dimension:
        locations = [location for location in locations if location["dimension"].lower().find(dimension) != -1]
    if at_least_residents:
        locations = [location for location in locations if len(location["residents"]) >= at_least_residents]
    return paginate_list(locations, page)


@router.get("/residents-sorted")
async def residents_sorted(token: Annotated[str, Depends(oauth2_scheme)],
                           page: int = 1,
                           verbose: bool = False):
    """
    All locations sorted by number of residents
    :param token:
    :param page:
    :param verbose:
    :return: List of locations
    """
    locations = cache.get_all_locations()
    locations = sorted(locations, key=lambda x: len(x["residents"]), reverse=True)
    if not verbose:
        locations = [{"name": location["name"], "resident_count": len(location["residents"])} for location in locations]
    return paginate_list(locations, page)


@router.get("/type-sorted")
async def type_sorted(token: Annotated[str, Depends(oauth2_scheme)],
                      page: int = 1,
                      verbose: bool = False):
    """
    All locations sorted by type
    :param token:
    :param page:
    :param verbose:
    :return: List of locations
    """
    locations = cache.get_all_locations()
    locations = sorted(locations, key=lambda x: x["type"], reverse=True)
    if not verbose:
        locations = [{"name": location["name"], "type": location["type"]} for location in locations]
    return paginate_list(locations, page)


@router.get("/most-common-dimension")
async def most_common_dimension(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Find the most common dimension among all locations
    :param token:
    :return: Most common dimension
    """
    locations = cache.get_all_locations()
    dimensions = {}
    for location in locations:
        if location["dimension"] in dimensions:
            dimensions[location["dimension"]] += 1
        else:
            dimensions[location["dimension"]] = 1
    most_common = max(dimensions, key=dimensions.get)
    return {"most_common_dimension": most_common, "count": dimensions[most_common]}
