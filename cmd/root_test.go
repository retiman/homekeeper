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
	assert.False(t, context.IsDebug)
	assert.True(t, context.IsQuiet)
	assert.True(t, context.IsDryRun)
}

func TestInitCommand(t *testing.T) {
	setupFixtures()
	initCommand.RunE = newTracingHandler(&calls.IsInitCalled)
	rootCommand.RunE = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{
		"init",
		"--git",
		"git@github.com:retiman/homekeeper.git",
	})

	rootCommand.Execute()

	assert.True(t, calls.IsInitCalled)
	assert.False(t, calls.IsRootCalled)
	assert.True(t, context.IsGit)
	assert.Equal(t, context.DotfilesLocation, "git@github.com:retiman/homekeeper.git")
}

func TestCleanupCommand(t *testing.T) {
	setupFixtures()
	cleanupCommand.RunE = newTracingHandler(&calls.IsCleanupCalled)
	rootCommand.RunE = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"cleanup"})

	rootCommand.Execute()

	assert.True(t, calls.IsCleanupCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, context.IsDebug)
	assert.False(t, context.IsDryRun)
}

func TestKeepCommand(t *testing.T) {
	setupFixtures()
	keepCommand.RunE = newTracingHandler(&calls.IsKeepCalled)
	rootCommand.RunE = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{
		"keep",
		"--dry-run",
		"--no-cleanup",
		"--no-overwrite",
	})

	rootCommand.Execute()

	assert.True(t, calls.IsKeepCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, context.IsDebug)
	assert.True(t, context.IsDryRun)
	assert.True(t, context.IsNoCleanup)
	assert.True(t, context.IsNoOverwrite)
}

func TestUnkeepCommand(t *testing.T) {
	setupFixtures()
	unkeepCommand.RunE = newTracingHandler(&calls.IsUnkeepCalled)
	rootCommand.RunE = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"unkeep"})

	rootCommand.Execute()

	assert.True(t, calls.IsUnkeepCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, context.IsDebug)
	assert.False(t, context.IsDryRun)
}

func TestVersionCommand(t *testing.T) {
	setupFixtures()
	versionCommand.RunE = newTracingHandler(&calls.IsVersionCalled)
	rootCommand.RunE = newTracingHandler(&calls.IsRootCalled)
	rootCommand.SetArgs([]string{"version"})

	rootCommand.Execute()

	assert.True(t, calls.IsVersionCalled)
	assert.False(t, calls.IsRootCalled)
	assert.False(t, context.IsDebug)
	assert.False(t, context.IsDryRun)
}
