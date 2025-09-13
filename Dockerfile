FROM golang:1.25-alpine3.22 AS builder

RUN apk add --no-cache make git ca-certificates && update-ca-certificates


WORKDIR /app

# Clone project
RUN git clone https://github.com/wtsi-hgi/movie-server.git .

# Copy Makefile
COPY Makefile .

# Build Go binary
RUN make build

FROM python:3.11-alpine

# Create non-root user
RUN adduser -D appuser

WORKDIR /app

# Create Python virtual environment
RUN python -m venv /opt/venv

# Upgrade pip and install requests inside venv
RUN /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir requests

# Add venv binaries to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Copy Go binary and Python client
COPY --from=builder /app/movie-server ./movie-server
COPY client.py ./client.py
COPY entrypoint.sh ./entrypoint.sh

# Make scripts executable
RUN chmod +x ./movie-server ./client.py ./entrypoint.sh

# Switch to non-root user
USER appuser

# Expose server port
EXPOSE 8080

# Set entrypoint and default command
ENTRYPOINT ["./entrypoint.sh"]
CMD ["server"]

