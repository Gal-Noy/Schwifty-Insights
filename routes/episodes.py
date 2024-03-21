from fastapi import APIRouter
from utils import paginate
import data.cache as cache

router = APIRouter()


@router.get("/filter")
async def filter_episodes(name: str = None,
                          episode: str = None,
                          character_ids: str = None,
                          page: int = 1):
    """
    Filter episodes by various parameters
    """
    episodes = cache.get_all_episodes()

    if name:
        episodes = [episode for episode in episodes if episode["name"].lower().find(name) != -1]
    if episode:
        episodes = [episode for episode in episodes if episode["episode"].lower().find(episode) != -1]
    if character_ids:
        character_ids = character_ids.split(",")
        episodes = [episode for episode in episodes if
                    all([character_id in [character.split("/")[-1] for character in episode["characters"]]
                         for character_id in character_ids])]
    return paginate(episodes, page)


@router.get("/character-count-sorted")
async def character_count_sorted(page: int = 1,
                                 verbose: bool = False):
    """
    All episodes sorted by most characters
    """
    episodes = cache.get_all_episodes()
    episodes = sorted(episodes, key=lambda x: len(x["characters"]), reverse=True)
    if not verbose:
        episodes = [{"name": episode["name"], "character_count": len(episode["characters"])} for episode in episodes]
    return paginate(episodes, page)


@router.get("/air-date-sorted")
async def air_date_sorted(page: int = 1,
                          verbose: bool = False):
    """
    All episodes sorted by air date
    """
    episodes = cache.get_all_episodes()
    episodes = sorted(episodes, key=lambda x: x["air_date"], reverse=True)
    if not verbose:
        episodes = [{"name": episode["name"], "air_date": episode["air_date"]} for episode in episodes]
    return paginate(episodes, page)
