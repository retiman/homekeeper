package common

import (
	"os"

	logger "github.com/apsdehal/go-logger"
)

func NewLogger(pkg string) *logger.Logger {
	newlog, err := logger.New(pkg, 0 /* color */, os.Stderr)
	if err != nil {
		panic(err)
	}

	setInfoLevel(newlog)
	return newlog
}

func SetDebugLevel(arg *logger.Logger) {
	setDebugLevel(arg)
	setDebugLevel(log)
}

func SetInfoLevel(arg *logger.Logger) {
	setInfoLevel(arg)
	setInfoLevel(log)
}

func setDebugLevel(arg *logger.Logger) {
	arg.SetLogLevel(logger.DebugLevel)
	arg.SetFormat("[%{lvl}] [%{file}:%{line}] %{message}")
}

func setInfoLevel(arg *logger.Logger) {
	arg.SetLogLevel(logger.InfoLevel)
	arg.SetFormat("%{message}")
}
