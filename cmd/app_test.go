package cmd

import (
	logger "github.com/apsdehal/go-logger"
	"github.com/retiman/homekeeper/pkg/common"
)

func init() {
	log.SetLogLevel(logger.DebugLevel)
	log.SetFormat(common.DebugFormat)
}
