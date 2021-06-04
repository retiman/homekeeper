package cmd

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCleanupDefaults(t *testing.T) {
	isCmdCalled := false
	isRootCalled := false
	app := New()

	app.cleanupCommand.Run = NewTracingHandler(&isCmdCalled)
	app.rootCommand.Run = NewTracingHandler(&isRootCalled)
	app.rootCommand.SetArgs([]string{"cleanup"})
	app.rootCommand.Execute()

	assert.True(t, isCmdCalled)
	assert.False(t, isRootCalled)
}
