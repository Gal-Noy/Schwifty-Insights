from cachetools import TTLCache
import data.client as client

CACHE_SIZE = 1000
CACHE_TTL = 60 * 60 * 24

cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TTL)


def get_all_characters():
    if "characters" in cache:
        return cache["characters"]
    else:
        characters = client.fetch_all_characters()
        cache["characters"] = characters
        return characters


def get_all_locations():
    if "locations" in cache:
        return cache["locations"]
    else:
        locations = client.fetch_all_locations()
        cache["locations"] = locations
        return locations


def get_all_episodes():
    if "episodes" in cache:
        return cache["episodes"]
    else:
        episodes = client.fetch_all_episodes()
        cache["episodes"] = episodes
        return episodes


def clear_cache():
    cache.clear()