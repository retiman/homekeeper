package cmd

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestRoot(t *testing.T) {
	isCmdCalled := false
	app := New()

	app.rootCommand.Run = NewTracingHandler(&isCmdCalled)
	app.rootCommand.SetArgs([]string{
		"--debug",
		"--dry-run",
	})
	app.rootCommand.Execute()

	assert.True(t, isCmdCalled)
	assert.True(t, app.flags.IsDebug)
	assert.True(t, app.flags.IsDryRun)
}
