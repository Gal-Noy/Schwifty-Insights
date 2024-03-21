from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_filter_characters():
    response = client.get("/characters/filter")
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Rick Sanchez"

    response = client.get("/characters/filter?name=rick%20sanchez&status=alive&species=human&gender=male&origin=137")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert "Rick Sanchez" in [character["name"] for character in response.json()]
    assert "Alive" in [character["status"] for character in response.json()]
    assert "Human" in [character["species"] for character in response.json()]
    assert "Male" in [character["gender"] for character in response.json()]


def test_appearances_sorted():
    response = client.get("/characters/appearances-sorted")
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Rick Sanchez"
    assert response.json()[0]["appearances"] == 51

    response = client.get("/characters/appearances-sorted?page=2")
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Traflorkian"
    assert response.json()[0]["appearances"] == 5


def test_status_sorted():
    response = client.get("/characters/status-sorted")
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Rick Sanchez"
    assert response.json()[0]["status"] == "Alive"

    response = client.get("/characters/status-sorted?page=30")
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "SEAL Team Rick"
    assert response.json()[0]["status"] == "Dead"


def test_species_sorted():
    response = client.get("/characters/species-sorted")
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Abadango Cluster Princess"
    assert response.json()[0]["species"] == "Alien"

    response = client.get("/characters/species-sorted?page=41")
    assert response.status_code == 200
    assert len(response.json()) == 20
    assert response.json()[0]["name"] == "Too Cute to Murder Beth"
    assert response.json()[0]["species"] == "Robot"


def test_most_common_species():
    response = client.get("/characters/most-common-species")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()["most_common_species"] == "Human"


