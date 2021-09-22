MODULE = github.com/retiman/homekeeper
BUILD = $(shell git rev-parse --short HEAD)
VERSION = $(file < VERSION)
.PHONY = all build format test

.PHONY: all
all: clean build format test

.PHONY: clean
clean:
	-$(RM) ./tmp
	-$(RM) ./homekeeper
	-$(RM) ./homekeeper.exe

.PHONY: download
download:
	@go install github.com/golangci/golangci-lint/cmd/golangci-lint@v1.42.1
	@go mod tidy

.PHONY: format
format:
	@gofmt -w -s cmd
	@gofmt -w -s pkg

.PHONY: lint
lint:
	@golangci-lint run ./...

.PHONY: build
build: format lint
	@go build -ldflags="-X '$(MODULE)/cmd.Build=$(BUILD)' -X '$(MODULE)/cmd.Version=$(VERSION)'" .

.PHONY: test
test: build
	@go test -v ./...
