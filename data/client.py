import os
import requests

# API_URL = os.environ.get('API_URL')

API_URL = "https://rickandmortyapi.com/api"


def fetch_locations():
    url = f"{API_URL}/location/"
    response = requests.get(url)
    return response.json()


def fetch_characters():
    url = f"{API_URL}/character/"
    response = requests.get(url)
    return response.json()


def fetch_episodes():
    url = f"{API_URL}/episode/"
    response = requests.get(url)
    return response.json()

