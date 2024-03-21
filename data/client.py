import os
import requests

# API_URL = os.environ.get('API_URL')

API_URL = "https://rickandmortyapi.com/api"


def fetch_all_characters():
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
    url = f"{API_URL}/character/{character_id}"
    response = requests.get(url)
    return response.json()


def fetch_all_locations():
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
    url = f"{API_URL}/location/{location_id}"
    response = requests.get(url)
    return response.json()


def fetch_all_episodes():
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
    url = f"{API_URL}/episode/{episode_id}"
    response = requests.get(url)
    return response.json()

