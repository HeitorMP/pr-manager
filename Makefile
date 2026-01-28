.PHONY: build run install clean test help

BINARY_NAME=pr-manager
build:
	@echo "Building..."
	go build -o $(BINARY_NAME) main.go

run: build
	./$(BINARY_NAME)

install:
	@echo "Installing..."
	go install

clean:
	@echo "Cleaning..."
	go clean
	rm -f $(BINARY_NAME)

deps:
	@echo "Downloading dependencies..."
	go mod download
	go mod tidy

test:
	@echo "Running tests..."
	go test -v ./...

fmt:
	@echo "Formatting code..."
	go fmt ./...

lint:
	@echo "Running linter..."
	golangci-lint run

help:
	@echo "Available targets:"
	@echo "  build    - Build the application"
	@echo "  run      - Run the application"
	@echo "  install  - Install the application globally"
	@echo "  clean    - Clean build artifacts"
	@echo "  deps     - Download and tidy dependencies"
	@echo "  test     - Run tests"
	@echo "  fmt      - Format code"
	@echo "  lint     - Run linter"
	@echo "  help     - Show this help message"
