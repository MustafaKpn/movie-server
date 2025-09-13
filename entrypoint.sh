#!/bin/sh
set -e

if [ "$1" = "client" ]; then
    shift
    echo "Starting movie server in background..."
    ./movie-server &
    SERVER_PID=$!

    # Wait for server to be ready (max 30 seconds)
    echo "Waiting for server to be ready on port 8080..."
    TRIES=0
    MAX_TRIES=30
    until nc -z localhost 8080; do
        sleep 1
        TRIES=$((TRIES + 1))
        if [ "$TRIES" -ge "$MAX_TRIES" ]; then
            echo "Error: server did not start in time!"
            kill $SERVER_PID
            exit 1
        fi
    done

    echo "Server is ready. Running Python client with args: $@"
    ./client.py "$@"

    # Kill server after client is done
    kill $SERVER_PID
else
    echo "Starting movie server (foreground)..."
    exec ./movie-server
fi

