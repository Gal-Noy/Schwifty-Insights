import os
import requests

# API_URL = os.environ.get('API_URL')

API_URL = "https://rickandmortyapi.com/api"


def fetch_all_characters():
    """
    Fetch all characters from the API
    :return:  List of characters
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


def fetch_single_character(character_id):
    """
    Fetch a single character by ID
    :param character_id:
    :return:  Character data
    """
    url = f"{API_URL}/character/{character_id}"
    response = requests.get(url)
    return response.json()


def fetch_all_locations():
    """
    Fetch all locations from the API
    :return:  List of locations
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


def fetch_single_location(location_id):
    """
    Fetch a single location by ID
    :param location_id:
    :return:  Location data
    """
    url = f"{API_URL}/location/{location_id}"
    response = requests.get(url)
    return response.json()


def fetch_all_episodes():
    """
    Fetch all episodes from the API
    :return:  List of episodes
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


def fetch_single_episode(episode_id):
    """
    Fetch a single episode by ID
    :param episode_id:  Episode ID
    :return:
    """
    url = f"{API_URL}/episode/{episode_id}"
    response = requests.get(url)
    return response.json()

