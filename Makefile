VERSION = $(file < VERSION)
.PHONY = all dist test

all: dist test

dist:
	@gofmt -w .
	@go build -ldflags="-X 'github.com/retiman/homekeeper/cmd.buildVersion=$(VERSION)'" .

test:
	@go test -v ./...
