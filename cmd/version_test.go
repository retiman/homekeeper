package cmd

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestVersionCommand(t *testing.T) {
	setupTest()
	versionCommand.Run = newTracingHandler(&calls.IsVersionCalled)
	rootCommand.Run = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"version"})

	rootCommand.Execute()

	assert.True(t, calls.IsVersionCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, flags.IsDebug)
	assert.False(t, flags.IsDryRun)
}
