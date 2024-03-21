from fastapi import APIRouter
from utils import paginate
import data.cache as cache

router = APIRouter()


@router.get("/filter")
async def filter_locations():
    """
    Filter locations by criteria
    """
    return {"message": "Filter locations by criteria"}


@router.get("/residents-sorted")
async def residents_sorted():
    """
    All locations sorted by most residents
    """
    return {"message": "All locations sorted by most residents"}


@router.get("/type-sorted")
async def type_sorted():
    """
    All locations sorted by type
    """
    return {"message": "All locations sorted by type"}


@router.get("/most-common-dimension")
async def most_common_dimension():
    """
    Most common dimension
    """
    return {"message": "Most common dimension"}
