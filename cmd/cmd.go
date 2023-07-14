package cmd

import (
	"io"
	"strings"

	logger "github.com/apsdehal/go-logger"
	"github.com/retiman/homekeeper/pkg/common"
)

var (
	// This build version will be set by reading the VERSION file in the repository root at build time (see the Makefile).
	Build   string
	Version string
	log     *logger.Logger
)

// In golang, init() functions are run in lexical file name order.  Renaming files can cause the init functions to
// execute in a different order, which may produce unintended effects (for example, we'd like the log to be defined
// first).  Therefore, the convention in this project is to only have init() functions in the go files with the same
// name as the package.
func init() {
	Build = strings.TrimSpace(Build)
	Version = strings.TrimSpace(Version)
	log = common.NewLogger("cmd", io.Discard)

	setup()
}
