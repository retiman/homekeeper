package cmd

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestRootCommand(t *testing.T) {
	setupTest()
	rootCommand.Run = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{
		"--debug",
		"--dry-run",
	})

	rootCommand.Execute()

	assert.True(t, calls.IsRootCalled)
	assert.True(t, flags.IsDebug)
	assert.True(t, flags.IsDryRun)
}
