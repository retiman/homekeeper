package cmd

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestVersion(t *testing.T) {
	isCmdCalled := false
	isRootCalled := false
	app := New()

	app.versionCommand.Run = NewTracingHandler(&isCmdCalled)
	app.rootCommand.Run = NewTracingHandler(&isRootCalled)
	app.rootCommand.SetArgs([]string{"version"})
	app.rootCommand.Execute()

	assert.True(t, isCmdCalled)
	assert.False(t, isRootCalled)
}
