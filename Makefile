VERSION = $(file < VERSION)
.PHONY = all dist test

all: dist format test

dist: format
	@go build -ldflags="-X 'github.com/retiman/homekeeper/cmd.buildVersion=$(VERSION)'" .

format:
	@gofmt -w -s cmd
	@gofmt -w -s pkg

test:
	@go test -v ./...
