import os

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

BEARER_TOKEN = os.getenv('TEST_USER_BEARER_TOKEN')


def test_filter_characters():
    response = client.get("/characters/filter", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 20
    assert response.json()["data"][0]["name"] == "Rick Sanchez"

    response = client.get("/characters/filter?name=rick%20sanchez&status=alive&species=human&gender=male&origin=137",
                          headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert "Rick Sanchez" in [character["name"] for character in response.json()["data"]]
    assert "Alive" in [character["status"] for character in response.json()["data"]]
    assert "Human" in [character["species"] for character in response.json()["data"]]
    assert "Male" in [character["gender"] for character in response.json()["data"]]

    response = client.get("/characters/filter?page=-1", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 404


def test_appearances_sorted():
    response = client.get("/characters/appearances-sorted", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 20
    assert response.json()["data"][0]["name"] == "Rick Sanchez"
    assert response.json()["data"][0]["appearances"] == 51

    response = client.get("/characters/appearances-sorted?page=2", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 20
    assert response.json()["data"][0]["name"] == "Traflorkian"
    assert response.json()["data"][0]["appearances"] == 5

    response = client.get("/characters/appearances-sorted?page=100",
                          headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200

    response = client.get("/characters/appearances-sorted?page=-1", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 404


def test_status_sorted():
    response = client.get("/characters/status-sorted", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 20
    assert response.json()["data"][0]["name"] == "Rick Sanchez"
    assert response.json()["data"][0]["status"] == "Alive"

    response = client.get("/characters/status-sorted?page=30", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 20
    assert response.json()["data"][0]["name"] == "SEAL Team Rick"
    assert response.json()["data"][0]["status"] == "Dead"

    response = client.get("/characters/status-sorted?page=-1", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 404


def test_species_sorted():
    response = client.get("/characters/species-sorted", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 20
    assert response.json()["data"][0]["name"] == "Abadango Cluster Princess"
    assert response.json()["data"][0]["species"] == "Alien"

    response = client.get("/characters/species-sorted?page=41", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 20
    assert response.json()["data"][0]["name"] == "Too Cute to Murder Beth"
    assert response.json()["data"][0]["species"] == "Robot"


def test_most_common_species():
    response = client.get("/characters/most-common-species", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["most_common_species"] == "Human"
