from cachetools import cached, TTLCache

CACHE_SIZE = 1000
CACHE_TTL = 60 * 60 * 24

cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TTL)
