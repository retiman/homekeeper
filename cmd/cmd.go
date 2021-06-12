package cmd

import (
	"strings"

	logger "github.com/apsdehal/go-logger"
	"github.com/retiman/homekeeper/pkg/common"
)

var (
	// This build version will be set by reading the VERSION file in the repository root at build time (see the Makefile).
	buildVersion = "0.0.0"
	log          *logger.Logger
)

func init() {
	buildVersion = strings.TrimSpace(buildVersion)
	log = common.NewLogger("cmd")

	initialize()
}
