BINARY ?= movie-server
MAIN_PKG ?= .

.PHONY: default build install clean

default: build

build:
	@echo "[make] go generate (if any)..."
	@go generate $(MAIN_PKG) || true
	@echo "[make] go build -> $(BINARY)"
	@go build -v -o $(BINARY) $(MAIN_PKG)

install:
	@echo "[make] go generate (if any)..."
	@go generate $(MAIN_PKG) || true
	@echo "[make] go install $(MAIN_PKG)"
	@go install $(MAIN_PKG)

clean:
	@echo "[make] clean"
	@rm -f $(BINARY)

