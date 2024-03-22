import os

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

BEARER_TOKEN = os.getenv('TEST_USER_BEARER_TOKEN')


def test_characters_relationships():
    response = client.get("/insights/characters-relationships", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200


def test_dimension_species_diversity():
    response = client.get("/insights/dimension-species-diversity", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200


def test_dangerous_locations():
    response = client.get("/insights/dangerous-locations", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200


def test_species_survival():
    response = client.get("/insights/species-survival", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200


def test_native_species():
    response = client.get("/insights/native-species", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200


def test_gender_by_location_type():
    response = client.get("/insights/gender-by-location-type", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200


def test_frequent_travelers():
    response = client.get("/insights/frequent-travelers", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200

