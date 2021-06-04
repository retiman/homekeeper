package cmd

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestKeepFlags(t *testing.T) {
	isCmdCalled := false
	isRootCalled := false
	app := New()

	app.keepCommand.Run = NewTracingHandler(&isCmdCalled)
	app.rootCommand.Run = NewTracingHandler(&isRootCalled)
	app.rootCommand.SetArgs([]string{
		"keep",
		"--dry-run",
		"--no-cleanup",
	})
	app.rootCommand.Execute()

	assert.True(t, isCmdCalled)
	assert.False(t, isRootCalled)
	assert.True(t, app.flags.IsDryRun)
	assert.True(t, app.flags.IsNoCleanup)
}

func TestKeepDefaults(t *testing.T) {
	isCmdCalled := false
	isRootCalled := false
	app := New()

	app.keepCommand.Run = NewTracingHandler(&isCmdCalled)
	app.rootCommand.Run = NewTracingHandler(&isRootCalled)
	app.rootCommand.SetArgs([]string{"keep"})
	app.rootCommand.Execute()

	assert.True(t, isCmdCalled)
	assert.False(t, isRootCalled)
	assert.False(t, app.flags.IsNoCleanup)
}
