package common

import (
	"fmt"
	"io"
	"os"

	logger "github.com/apsdehal/go-logger"
)

var (
	log *logger.Logger
)

func NewLogger(pkg string, out io.Writer) *logger.Logger {
	newlog, err := logger.New(pkg, 0 /* color */, out)
	if err != nil {
		panic(err)
	}

	newlog.SetLogLevel(logger.DebugLevel)
	newlog.SetFormat("[%{lvl}] [%{file}:%{line}] %{message}")
	return newlog
}

func EnableLogging() {
	// This needs to be an exported function.  Otherwise the cmd package will not be able to enable/disable logging
	// (unless we export "log" as "Log").
	log = NewLogger("common", os.Stderr)
}

func WriteOutputf(format string, a ...interface{}) {
	if IsQuiet {
		return
	}

	fmt.Printf(format, a...)
}
