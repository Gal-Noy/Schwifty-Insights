import os

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

BEARER_TOKEN = os.getenv('TEST_USER_BEARER_TOKEN')


def test_filter_episodes():
    response = client.get("/episodes/filter", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Pilot"

    response = client.get("/episodes/filter?name=rixty%20minutes", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Rixty Minutes"
    assert response.json()[0]["episode"] == "S01E08"

    response = client.get("/episodes/filter?character_ids=1,3,5,7,14", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["episode"] == "S01E10"


def test_character_count_sorted():
    response = client.get("/episodes/character-count-sorted", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "The Ricklantis Mixup"
    assert response.json()[0]["character_count"] == 65

    response = client.get("/episodes/character-count-sorted?page=2", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "One Crew Over the Crewcoo's Morty"
    assert response.json()[0]["character_count"] == 23


def test_air_date_sorted():
    response = client.get("/episodes/air-date-sorted", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Forgetting Sarick Mortshall"
    assert response.json()[0]["air_date"] == "September 5, 2021"

    response = client.get("/episodes/air-date-sorted?page=2", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Raising Gazorpazorp"
    assert response.json()[0]["air_date"] == "March 10, 2014"
