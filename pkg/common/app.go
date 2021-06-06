package common

import (
	"os"

	logger "github.com/apsdehal/go-logger"
)

var (
	IsDryRun bool
	log      *logger.Logger
)

func init() {
	var err error
	log, err = logger.New("common", 1 /* color */, os.Stderr)
	if err != nil {
		panic(err)
	}

	log.SetLogLevel(logger.InfoLevel)
	log.SetFormat(InfoFormat)
}
