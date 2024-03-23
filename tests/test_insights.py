import os

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

BEARER_TOKEN = os.getenv('TEST_USER_BEARER_TOKEN')


# Notice that the tests are not testing the actual logic of the endpoints, but rather if the endpoints are working
# correctly. This is because the logic of the endpoints is already tested in the test_data_analysis.py file.

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


def test_interdimensional_travelers():
    response = client.get("/insights/interdimensional-travelers", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200


def test_frequent_travelers():
    response = client.get("/insights/frequent-travelers", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200


def test_main_characters():
    response = client.get("/insights/main-characters", headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    assert response.status_code == 200
