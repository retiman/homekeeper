package cmd

import (
	"os"

	"github.com/retiman/homekeeper/pkg/common"
	"github.com/spf13/cobra"
)

type Calls struct {
	IsRootCalled    bool
	IsCleanupCalled bool
	IsKeepCalled    bool
	IsUnkeepCalled  bool
	IsVersionCalled bool
}

var (
	calls *Calls
)

func init() {
	log = common.NewLogger("cmd", os.Stderr)
}

// Setup tests by resetting package state.  Note that writing a `TestMain` will not work as that setupFixtures/teardown will
// only once per package, not per test.
func setupFixtures() {
	calls = &Calls{}

	initialize()
}

// Create a command handler that can trace calls to it for Debugfging.  Use this to replace the run handler in a test
// so that running the command does not do something destructive.
func newTracingHandler(isCalled *bool) func(*cobra.Command, []string) error {
	return func(_ *cobra.Command, _ []string) (err error) {
		*isCalled = true
		return
	}
}
