# Movie Server

A Go-based movie server with a Python client for counting movies by year. The server provides an authenticated API for retrieving movie data, and the client can count movies for specific years.

## Prerequisites

- Docker installed on your system
- Git (for cloning the repository)

## Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:MustafaKpn/movie-server.git
cd movie-server
```

### 2. Build the Docker Image

```bash
docker build -t movie-server .
```

### 3. Run the Server

To run the server in the foreground:

```bash
docker run -p 8080:8080 movie-server
```

The server will be available at `http://localhost:8080`.

### 4. Run the Client

To run the client (which automatically starts the server in the background and stops it when done):

```bash
docker run movie-server client 1910 2000
```

This will count movies for the years 1910 and 2000.

## Client Usage

### Basic Examples

```bash
# Count movies for a single year
docker run movie-server client 2000

# Count movies for multiple years
docker run movie-server client 1901 1902 1905 2025
```

### Advanced Options

```bash
# Use custom authentication credentials
docker run movie-server client --username myuser --password mypass 2023

# Combine options
docker run movie-server client --server http://localhost:8080 --username admin --password secret 2020 2021
```

### Available Client Options

- `--server`: Base URL of the movie server (default: `http://localhost:8080`)
- `--username`: Authentication username (default: `username`)
- `--password`: Authentication password (default: `password`)

## Authentication

The server uses bearer token authentication with default credentials:

- **Username**: `username`
- **Password**: `password`

## Authentication

The server uses bearer token authentication with default credentials:

- **Username**: `username`
- **Password**: `password`

## Troubleshooting

### Port Already in Use

If you get a port binding error:

```bash
docker run -p 8081:8080 movie-server
```

### Container Issues

To see running containers:

```bash
docker ps
```

To stop a running container:

```bash
docker stop <container-id>
```

To remove the image and rebuild:

```bash
docker rmi movie-server
docker build -t movie-server .
```

## Testing Utilities

### 1. Test Docker Setup

You can use the included `test_docker.sh` script to verify that Docker builds the image correctly and that the server starts:

```bash
./test_docker.sh
```

### 2. Run Python Client Tests

The file `test_client.py` contains **unit tests** for the Python client logic.  
These tests are written with [pytest](https://docs.pytest.org/) and **do not require the server to be running**.

#### Run in a virtual environment (recommended)

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the dependencies:

```bash
pip install -r requirements.txt
pip install pytest
```

3. Run the tests:

```bash
pytest -v test_client.py
```

4. When finished, deactivate the virtual environment:

```bash
deactivate
```

This will validate:

- Authentication logic (using mocked responses)
- Movie counting logic
- Error handling

### 2. Run Python Client Tests

The file `test_client.py` contains **unit tests** for the Python client logic.  
These tests are written with [pytest](https://docs.pytest.org/) and **do not require the server to be running**.

#### Run in a virtual environment (recommended)

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the dependencies:

```bash
pip install -r requirements.txt
pip install pytest
```

3. Run the tests:

```bash
pytest -v test_client.py
```

4. When finished, deactivate the virtual environment:

```bash
deactivate
```

This will validate:

- Authentication logic (using mocked responses)
- Movie counting logic
- Error handling
