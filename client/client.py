#!/usr/bin/env python
import argparse
import requests
import sys

GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def authenticate(base_url, username, password):
    url = f"{base_url}/api/auth"
    payload = {"username": username, "password": password}
    resp = requests.post(url, json=payload)
    if resp.status_code != 200:
        raise RuntimeError(f"Auth failed: {resp.status_code} {resp.text}")
    return resp.json()["bearer"]

def count_movies(base_url, year, username, password):
    total = 0
    page = 1

    print(f"{CYAN}{BOLD}Counting movies for {year}{RESET}:")

    while True:
        token = authenticate(base_url, username, password)
        headers = {"Authorization": token}

        url = f"{base_url}/api/movies/{year}/{page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise RuntimeError(f"Request failed: {resp.status_code} {resp.text}")

        movies = resp.json()
        total += len(movies)

        print(f"{GREEN}Total movies so far: {total}{RESET}    ", end='\r', flush=True)

        if len(movies) < 10:
            break
        page += 1

    print(f"{CYAN}{BOLD}Total movies: {GREEN}{total}{RESET}            \n")
    return total


def main():
    parser = argparse.ArgumentParser(description="Movie counter client")
    parser.add_argument("years", metavar="YEAR", type=int, nargs="+",
                        help="One or more years to count movies for")
    parser.add_argument("--server", default="http://localhost:8080",
                        help="Base URL of the movie server (default: http://localhost:8080)")
    parser.add_argument("--username", default="username",
                        help="Auth username (default: username)")
    parser.add_argument("--password", default="password",
                        help="Auth password (default: password)")
    args = parser.parse_args()

    try:
        authenticate(args.server, args.username, args.password)
    except Exception as e:
        print(f"Authentication failed: {e}", file=sys.stderr)
        sys.exit(1)

    for year in args.years:
        try:
            count_movies(args.server, year, args.username, args.password)
        except Exception as e:
            print(f"{year}: error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()

