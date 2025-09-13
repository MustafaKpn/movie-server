import pytest
import requests
import requests_mock
from client import MovieClient


@pytest.fixture
def client():
    return MovieClient(base_url="http://fake-server", username="user", password="pass")


def test_authenticate(client):
    with requests_mock.Mocker() as m:
        m.post("http://fake-server/api/auth", json={"bearer": "fake-token"}, status_code=200)
        token = client.authenticate()
        assert token == "fake-token"


def test_count_movies(client):
    with requests_mock.Mocker() as m:
        m.post("http://fake-server/api/auth", json={"bearer": "fake-token"}, status_code=200)

        # Mock movies endpoint: page 1 has 3 movies
        m.get("http://fake-server/api/movies/2023/1", json=[{"title": "A"}, {"title": "B"}, {"title": "C"}], status_code=200)

        total = client.count_movies(2023)
        assert total == 3

