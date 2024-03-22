import os
from cachetools import TTLCache
import data.client as client

CACHE_SIZE = float(os.getenv("CACHE_SIZE"))
CACHE_TTL = float(os.getenv("CACHE_SIZE"))

cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TTL)


def get_all_characters():
    """
    Get all characters
    :return: List of characters
    """
    if "characters" in cache:
        return cache["characters"]
    else:
        characters = client.fetch_all_characters()
        cache["characters"] = characters
        return characters


def get_all_locations():
    """
    Get all locations
    :return: List of locations
    """
    if "locations" in cache:
        return cache["locations"]
    else:
        locations = client.fetch_all_locations()
        cache["locations"] = locations
        return locations


def get_all_episodes():
    """
    Get all episodes
    :return: List of episodes
    """
    if "episodes" in cache:
        return cache["episodes"]
    else:
        episodes = client.fetch_all_episodes()
        cache["episodes"] = episodes
        return episodes
