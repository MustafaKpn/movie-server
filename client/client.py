
import requests


def authenticate(base_url, username, password):
    url = f"{base_url}/api/auth"
    payload = {"username": username, "password": password}
    resp = requests.post(url, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"Auth failed: {resp.status_code} {resp.text}")
    return resp.json()["bearer"]

def count_movies(base_url, token, year):
    headers = {"Authorization": token}
    total = 0
    page = 1
    while True:
        url = f"{base_url}/api/movies/{year}/{page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise RuntimeError(f"Request failed: {resp.status_code} {resp.text}")
        movies = resp.json()
        n = len(movies)
        total += n
        if n < 10:
            break
        page += 1
    return total
