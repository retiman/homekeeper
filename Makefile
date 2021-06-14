MODULE = github.com/retiman/homekeeper
BUILD = $(shell git rev-parse --short HEAD)
VERSION = $(file < VERSION)
.PHONY = all dist format test

all: dist format test

dist: format
	@go build -ldflags="-X '$(MODULE)/cmd.Build=$(BUILD)' -X '$(MODULE)/cmd.Version=$(VERSION)'" .

format:
	@gofmt -w -s cmd
	@gofmt -w -s pkg

test:
	@go test -v ./...
