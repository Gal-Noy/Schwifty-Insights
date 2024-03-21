from fastapi import APIRouter
from utils import paginate
import data.cache as cache

router = APIRouter()


@router.get("/filter")
async def filter_characters(name: str = None,
                            status: str = None,
                            species: str = None,
                            type: str = None,
                            gender: str = None,
                            origin: str = None,
                            location: str = None,
                            page: int = 1):
    """
    Filter characters by criteria
    """
    characters = cache.get_all_characters()

    if name:
        characters = [character for character in characters if character["name"].lower().find(name) != -1]
    if status:
        characters = [character for character in characters if character["status"].lower().find(status) != -1]
    if species:
        characters = [character for character in characters if character["species"].lower().find(species) != -1]
    if type:
        characters = [character for character in characters if character["type"].lower().find(type) != -1]
    if gender:
        characters = [character for character in characters if character["gender"].lower().find(gender) != -1]
    if origin:
        characters = [character for character in characters if character["origin"]["name"].lower().find(origin) != -1]
    if location:
        characters = [character for character in characters if
                      character["location"]["name"].lower().find(location) != -1]

    return paginate(characters, page)


@router.get("/appearances-sorted")
async def appearances_sorted(page: int = 1,
                             verbose: bool = False):
    """
    All characters sorted by most appearances in episodes
    """
    characters = cache.get_all_characters()
    characters = sorted(characters, key=lambda x: len(x["episode"]), reverse=True)
    if not verbose:
        characters = [{"name": character["name"], "appearances": len(character["episode"])} for character in characters]
    return paginate(characters, page)


@router.get("/status-sorted")
async def status_sorted(page: int = 1,
                        verbose: bool = False):
    """
    All characters sorted by status
    """
    characters = cache.get_all_characters()
    characters = sorted(characters, key=lambda x: x["status"])
    if not verbose:
        characters = [{"name": character["name"], "status": character["status"]} for character in characters]
    return paginate(characters, page)


@router.get("/species-sorted")
async def species_sorted(page: int = 1,
                         verbose: bool = False):
    """
    All characters sorted by species
    """
    characters = cache.get_all_characters()
    characters = sorted(characters, key=lambda x: x["species"])
    if not verbose:
        characters = [{"name": character["name"], "species": character["species"]} for character in characters]
    return paginate(characters, page)


@router.get("/most-common-species")
async def most_common_species():
    """
    Most common species
    """
    characters = cache.get_all_characters()
    species = {}
    for character in characters:
        if character["species"] in species:
            species[character["species"]] += 1
        else:
            species[character["species"]] = 1
    return {"most_common_species": max(species, key=species.get)}
