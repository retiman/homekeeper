package logging

import (
	"os"

	logger "github.com/apsdehal/go-logger"
)

var (
	// Normally go-logger expects you to create one logger instance per package, configuring defaults on the go-logger
	// package.  However, we'd like to modify the log level and format for all created loggers at runtime, based on user
	// input (we'd also like to enable debug level during tests).  This would make managing loggers pretty complicated,
	// but we can simplify things by re-using the same logger in every package, by referencing this one, and setting the
	// module to be "DEFAULT".
	Log = newDefaultLogger()
)

// Sets the log level and format for all loggers that use this package.  There's no need to restore the default logger
// as there's no need to switch back and forth between debug/non-debug mode at runtime.
func SetDebugLevel() {
	Log = newDebugLogger()
}

func newDebugLogger() *logger.Logger {
	log, err := logger.New("DEFAULT", 1 /* color */, os.Stderr)
	if err != nil {
		panic(err)
	}

	log.SetFormat("[%{level}] %{file}:%{line} %{message}")
	log.SetLogLevel(logger.DebugLevel)
	return log
}

func newDefaultLogger() *logger.Logger {
	log, err := logger.New("DEFAULT", 1 /* color */, os.Stderr)
	if err != nil {
		panic(err)
	}

	log.SetFormat("%{message}")
	log.SetLogLevel(logger.InfoLevel)
	return log
}
