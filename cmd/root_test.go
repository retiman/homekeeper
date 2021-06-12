package cmd

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestRootCommand(t *testing.T) {
	setupFixtures()
	rootCommand.RunE = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{
		"--debug",
		"--quiet",
		"--dry-run",
	})

	rootCommand.Execute()

	assert.True(t, calls.IsRootCalled)
	assert.True(t, flags.IsDebug)
	assert.True(t, flags.IsQuiet)
	assert.True(t, flags.IsDryRun)
}

func TestCleanupCommand(t *testing.T) {
	setupFixtures()
	cleanupCommand.RunE = newTracingHandler(&calls.IsCleanupCalled)
	rootCommand.RunE = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"cleanup"})

	rootCommand.Execute()

	assert.True(t, calls.IsCleanupCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, flags.IsDebug)
	assert.False(t, flags.IsDryRun)
}

func TestKeepCommand(t *testing.T) {
	setupFixtures()
	keepCommand.RunE = newTracingHandler(&calls.IsKeepCalled)
	rootCommand.RunE = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"keep"})

	rootCommand.Execute()

	assert.True(t, calls.IsKeepCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, flags.IsDebug)
	assert.False(t, flags.IsDryRun)
}

func TestUnkeepCommand(t *testing.T) {
	setupFixtures()
	unkeepCommand.RunE = newTracingHandler(&calls.IsUnkeepCalled)
	rootCommand.RunE = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"unkeep"})

	rootCommand.Execute()

	assert.True(t, calls.IsUnkeepCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, flags.IsDebug)
	assert.False(t, flags.IsDryRun)
}

func TestVersionCommand(t *testing.T) {
	setupFixtures()
	versionCommand.RunE = newTracingHandler(&calls.IsVersionCalled)
	rootCommand.RunE = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"version"})

	rootCommand.Execute()

	assert.True(t, calls.IsVersionCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, flags.IsDebug)
	assert.False(t, flags.IsDryRun)
}
