#!/usr/bin/env python
import argparse
import requests
import sys

GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class MovieClient:
    """Client for interacting with the movie server API."""

    def __init__(self, base_url: str, username: str, password: str):
        """
        Initialize the MovieClient.
        
        Args:
            base_url: The base URL of the movie server
            username: Authentication username
            password: Authentication password
        """

        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None

    def authenticate(self):
        """
        Authenticate with the server and get a bearer token.
        
        Returns:
            Bearer token for API requests
            
        Raises:
            RuntimeError: If authentication fails
        """

        url = f"{self.base_url}/api/auth"
        payload = {"username": self.username, "password": self.password}
        resp = requests.post(url, json=payload)
        if resp.status_code != 200:
            raise RuntimeError(f"Auth failed: {resp.status_code} {resp.text}")
        self.token = resp.json()["bearer"]
        return self.token
    


    def count_movies(self, year):
        """
        Count all movies for a specific year.
        
        Args:
            year: The year to count movies for
            
        Returns:
            Total number of movies for the year
            
        Raises:
            RuntimeError: If the request fails
        """

        total = 0
        page = 1

        print(f"{CYAN}{BOLD}Counting movies for {year}{RESET}:")

        while True:
            token = self.authenticate()
            headers = {"Authorization": token}

            url = f"{self.base_url}/api/movies/{year}/{page}"
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
    """Main entry point for the movie client."""
    
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
    client = MovieClient(args.server, args.username, args.password)

    try:
        client.authenticate()
    except Exception as e:
        print(f"Authentication failed: {e}", file=sys.stderr)
        sys.exit(1)

    for year in args.years:
        try:
            client.count_movies(year)
        except Exception as e:
            print(f"{year}: error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()

