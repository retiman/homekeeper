MODULE = github.com/retiman/homekeeper
BUILD = $(shell git rev-parse --short HEAD)
VERSION = $(file < VERSION)
.PHONY = all build format test

all: clean build format test

clean:
	-$(RM) ./tmp
	-$(RM) ./homekeeper
	-$(RM) ./homekeeper.exe

build: format
	@go build -ldflags="-X '$(MODULE)/cmd.Build=$(BUILD)' -X '$(MODULE)/cmd.Version=$(VERSION)'" .

format:
	@gofmt -w -s cmd
	@gofmt -w -s pkg

test:
	@go test -v ./...
