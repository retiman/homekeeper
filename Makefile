MODULE = github.com/retiman/homekeeper
BUILD = $(shell git rev-parse --short HEAD)
VERSION = $(file < VERSION)
.PHONY: all clean deps format lint build test

all: clean build format test

clean:
	-$(RM) -r ./tmp
	-$(RM) ./homekeeper
	-$(RM) ./homekeeper.exe

format:
	@gofmt -w -s cmd
	@gofmt -w -s pkg

check:
	@golangci-lint run ./...
	@goreleaser check
	

build:
	@go build -ldflags="-X '$(MODULE)/cmd.Build=$(BUILD)' -X '$(MODULE)/cmd.Version=$(VERSION)'" .

test: build
	@go test -v ./...

tag: format lint build
	git tag -a v${VERSION} -m "v${VERSION}"
