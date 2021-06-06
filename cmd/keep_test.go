package cmd

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestKeepCommand(t *testing.T) {
	setupTest()
	keepCommand.Run = newTracingHandler(&calls.IsKeepCalled)
	rootCommand.Run = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"keep"})

	rootCommand.Execute()

	assert.True(t, calls.IsKeepCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, flags.IsDebug)
	assert.False(t, flags.IsDryRun)
}
