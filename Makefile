MODULE := github.com/retiman/homekeeper
BUILD = $(shell git rev-parse --short HEAD)
VERSION = $(file < VERSION)

ifeq ($(OS),Windows_NT)
	SHELL := powershell.exe
	.SHELLFLAGS := -COMMAND
	RM := Remove-Item -Recurse -Force -ErrorAction Ignore
else
	RM := rm -rf
endif

.PHONY: all
all: clean lint format build test

.PHONY: clean
clean:
	-$(RM) ./tmp
	-$(RM) ./homekeeper
	-$(RM) ./homekeeper.exe

.PHONY: lint
lint:
	@go mod verify

.PHONY: format
format:
	@gofmt -w -s .

.PHONY: build
build:
	@go build -ldflags="-X '$(MODULE)/cmd.Build=$(BUILD)' -X '$(MODULE)/cmd.Version=$(VERSION)'" .

.PHONY: test
test: build
	@go test -v ./...

.PHONY: tag
tag: lint format build test
	@git tag -a v${VERSION} -m "v${VERSION}"
	@echo "Now git push --tags to create a release."

.PHONY: deps
deps:
	@go get -u ./...

.PHONY: tidy
tidy:
	@go mod tidy