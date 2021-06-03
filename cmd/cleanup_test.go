package cmd

import (
	"github.com/stretchr/testify/assert"
	"testing"
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
