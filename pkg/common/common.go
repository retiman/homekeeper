package common

import (
	logger "github.com/apsdehal/go-logger"
)

var (
	IsDryRun bool
	log      *logger.Logger
)

func init() {
	log = NewLogger("common")
}
