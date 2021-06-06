package common

import (
	"os"

	logger "github.com/apsdehal/go-logger"
)

var (
	log = NewDefaultLogger()
)

func NewDebugLogger() *logger.Logger {
	log, err := logger.New("DEFAULT", 1 /* color */, os.Stderr)
	if err != nil {
		panic(err)
	}

	log.SetFormat("[%{level}] %{file}:%{line} %{message}")
	log.SetLogLevel(logger.DebugLevel)
	return log
}

func NewDefaultLogger() *logger.Logger {
	log, err := logger.New("DEFAULT", 1 /* color */, os.Stderr)
	if err != nil {
		panic(err)
	}

	log.SetFormat("%{message}")
	log.SetLogLevel(logger.InfoLevel)
	return log
}

func SetDebugLogger() {
	log = NewDebugLogger()
}
