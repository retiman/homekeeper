package cmd

import (
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

type CommandHandler func(*cobra.Command, []string)

var (
	calls *Calls
)

func init() {
	log = common.NewDebugLogger()
}

// Setup tests by resetting package state.  Note that writing a `TestMain` will not work as that setupTest/teardown will
// only once per package, not per test.
func setupTest() {
	flags = &Flags{}
	calls = &Calls{}
	initCommands()
}

// Create a command handler that can trace calls to it for debugging.  Use this to replace the run handler in a test
// so that running the command does not do something destructive.
func newTracingHandler(isCalled *bool) CommandHandler {
	return func(_ *cobra.Command, _ []string) {
		*isCalled = true
	}
}
