#!/bin/bash

set -e

echo "Testing Docker build..."
docker build -t movie-server .

echo "Testing server mode..."
docker run -d --name test-server -p 8080:8080 movie-server server
sleep 5

if nc -z localhost 8080; then
    echo "Server is running on port 8080"
else
    echo "Server failed to start"
    exit 1
fi

docker stop test-server 1> /dev/null
docker rm test-server 1> /dev/null

echo "Docker test passed - container builds and server starts correctly"
