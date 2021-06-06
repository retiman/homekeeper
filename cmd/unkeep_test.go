package cmd

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestUnkeepCommand(t *testing.T) {
	setupTest()
	unkeepCommand.Run = newTracingHandler(&calls.IsUnkeepCalled)
	rootCommand.Run = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"unkeep"})

	rootCommand.Execute()

	assert.True(t, calls.IsUnkeepCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, flags.IsDebug)
	assert.False(t, flags.IsDryRun)
}
