from cachetools import TTLCache
from client import fetch_characters, fetch_episodes, fetch_locations

CACHE_SIZE = 1000
CACHE_TTL = 60 * 60 * 24

cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TTL)


def get_characters():
    cached_characters = cache.get("characters")
    if cached_characters:
        return cached_characters
    else:
        characters = fetch_characters()
        cache["characters"] = characters
        return characters


def get_episodes():
    cached_episodes = cache.get("episodes")
    if cached_episodes:
        return cached_episodes
    else:
        episodes = fetch_episodes()
        cache["episodes"] = episodes
        return episodes


def get_locations():
    cached_locations = cache.get("locations")
    if cached_locations:
        return cached_locations
    else:
        locations = fetch_locations()
        cache["locations"] = locations
        return locations
