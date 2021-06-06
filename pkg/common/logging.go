package common

import (
	logger "github.com/apsdehal/go-logger"
)

const (
	DebugFormat = "[%{level}] %{module}:%{file}:%{line} %{message}"
	InfoFormat  = "%{message}"
)

func SetLogLevel(level logger.LogLevel) {
	log.SetLogLevel(level)
}

func SetLogFormat(format string) {
	log.SetFormat(format)
}
