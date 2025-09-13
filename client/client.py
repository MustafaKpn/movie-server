
import requests


def authenticate(base_url, username, password):
    url = f"{base_url}/api/auth"
    payload = {"username": "username", "password": "password"}
    resp = requests.post(url, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"Auth failed: {resp.status_code} {resp.text}")
    return resp.json()["bearer"]
