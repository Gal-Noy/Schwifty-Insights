from typing import List

from pydantic import BaseModel, HttpUrl


class Character(BaseModel):
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    origin: dict  # Name and URL
    location: dict  # Name and URL
    image: HttpUrl
    episode: List[HttpUrl]
    url: HttpUrl
    created: str


class Location(BaseModel):
    id: int
    name: str
    type: str
    dimension: str
    residents: List[HttpUrl]
    url: HttpUrl
    created: str


class Episode(BaseModel):
    id: int
    name: str
    air_date: str
    episode: str
    characters: List[HttpUrl]
    url: HttpUrl
    created: str
