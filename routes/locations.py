from fastapi import APIRouter
from utils import paginate_list
import data.cache as cache

router = APIRouter()


@router.get("/filter")
async def filter_locations(name: str = None,
                           type: str = None,
                           dimension: str = None,
                           at_least_residents: int = None,
                           page: int = 1):
    """
    Filter locations by various parameters
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
async def residents_sorted(page: int = 1,
                           verbose: bool = False):
    """
    All locations sorted by most residents
    """
    locations = cache.get_all_locations()
    locations = sorted(locations, key=lambda x: len(x["residents"]), reverse=True)
    if not verbose:
        locations = [{"name": location["name"], "resident_count": len(location["residents"])} for location in locations]
    return paginate_list(locations, page)


@router.get("/type-sorted")
async def type_sorted(page: int = 1,
                        verbose: bool = False):
    """
    All locations sorted by type
    """
    locations = cache.get_all_locations()
    locations = sorted(locations, key=lambda x: x["type"], reverse=True)
    if not verbose:
        locations = [{"name": location["name"], "type": location["type"]} for location in locations]
    return paginate_list(locations, page)


@router.get("/most-common-dimension")
async def most_common_dimension():
    """
    Most common dimension
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
