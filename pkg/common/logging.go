package common

import (
	"fmt"
	"io"

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

func WriteOutput(ctx *Context, format string, a ...interface{}) {
	if ctx.IsQuiet {
		return
	}

	fmt.Printf(format, a...)
}
