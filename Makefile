MODULE = github.com/retiman/homekeeper
BUILD = $(shell git rev-parse --short HEAD)
VERSION = $(file < VERSION)
.PHONY = all build format test

all: build format test

build: format
	@go build -ldflags="-X '$(MODULE)/cmd.Build=$(BUILD)' -X '$(MODULE)/cmd.Version=$(VERSION)'" .

format:
	@gofmt -w -s cmd
	@gofmt -w -s pkg

test:
	@go test -v ./...
