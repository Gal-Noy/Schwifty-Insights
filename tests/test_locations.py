import os

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

BEARER_TOKEN = os.getenv('TEST_USER_BEARER_TOKEN')


def test_filter_locations():
    response = client.get("/locations/filter", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Earth (C-137)"

    response = client.get("/locations/filter?type=planet&at_least_residents=40", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Earth (Replacement Dimension)"

    response = client.get("/locations/filter?page=2", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Testicle Monster Dimension"


def test_residents_sorted():
    response = client.get("/locations/residents-sorted", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Earth (Replacement Dimension)"
    assert response.json()[0]["resident_count"] == 230

    response = client.get("/locations/residents-sorted?page=2", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Unity's Planet"
    assert response.json()[0]["resident_count"] == 6


def test_type_sorted():
    response = client.get("/locations/type-sorted", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Signus 5 Expanse"
    assert response.json()[0]["type"] == "unknown"

    response = client.get("/locations/type-sorted?page=2", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Z. Q. P. D."
    assert response.json()[0]["type"] == "Police Department"


def test_most_common_dimension():
    response = client.get("/locations/most-common-dimension", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()["most_common_dimension"] == "Replacement Dimension"
    assert response.json()["count"] == 57

