MODULE = github.com/retiman/homekeeper
BUILD = $(shell git rev-parse --short HEAD)
VERSION = $(file < VERSION)

.PHONY: all
all: clean check format build test

.PHONY: clean
clean:
	-$(RM) -r ./tmp
	-$(RM) ./homekeeper
	-$(RM) ./homekeeper.exe

.PHONY: check
check:
	@go mod verify
	@golangci-lint run ./...
	@goreleaser check

.PHONY: format
format:
	@gofmt -w -s cmd
	@gofmt -w -s pkg

.PHONY: build
build:
	@go build -ldflags="-X '$(MODULE)/cmd.Build=$(BUILD)' -X '$(MODULE)/cmd.Version=$(VERSION)'" .

.PHONY: test
test: build
	@go test -v ./...

.PHONY: tag
tag: format lint build test
	@git tag -a v${VERSION} -m "v${VERSION}"
	@echo "Now git push --tags to create a release."
