MODULE = github.com/retiman/homekeeper
BUILD = $(shell git rev-parse --short HEAD)
VERSION = $(file < VERSION)
.PHONY: all clean deps format lint build test

all: clean build format test

clean:
	-$(RM) -r ./tmp
	-$(RM) ./homekeeper
	-$(RM) ./homekeeper.exe

deps:
	@go install github.com/golangci/golangci-lint/cmd/golangci-lint@v1.46.1
	@go mod tidy

format:
	@gofmt -w -s cmd
	@gofmt -w -s pkg

lint:
	@golangci-lint run ./...

build:
	@go build -ldflags="-X '$(MODULE)/cmd.Build=$(BUILD)' -X '$(MODULE)/cmd.Version=$(VERSION)'" .

test: build
	@go test -v ./...
