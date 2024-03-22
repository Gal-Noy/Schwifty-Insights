import os
import requests

API_URL = os.getenv('API_URL')


def fetch_all_characters():
    """
    Fetch all characters from the API
    :return: List of characters
    """
    page = 1
    characters = []
    while True:
        url = f"{API_URL}/character/?page={page}"
        response = requests.get(url)
        data = response.json()
        if data and 'results' in data:
            characters.extend(data["results"])
            page += 1
        else:
            break
    return characters


def fetch_all_locations():
    """
    Fetch all locations from the API
    :return: List of locations
    """
    page = 1
    locations = []
    while True:
        url = f"{API_URL}/location/?page={page}"
        response = requests.get(url)
        data = response.json()
        if data and 'results' in data:
            locations.extend(data["results"])
            page += 1
        else:
            break
    return locations


def fetch_all_episodes():
    """
    Fetch all episodes from the API
    :return: List of episodes
    """
    page = 1
    episodes = []
    while True:
        url = f"{API_URL}/episode/?page={page}"
        response = requests.get(url)
        data = response.json()
        if data and 'results' in data:
            episodes.extend(data["results"])
            page += 1
        else:
            break
    return episodes
