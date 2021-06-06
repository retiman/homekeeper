package cmd

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCleanupCommand(t *testing.T) {
	setupTest()
	cleanupCommand.Run = newTracingHandler(&calls.IsCleanupCalled)
	rootCommand.Run = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"cleanup"})

	rootCommand.Execute()

	assert.True(t, calls.IsCleanupCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, flags.IsDebug)
	assert.False(t, flags.IsDryRun)
}
