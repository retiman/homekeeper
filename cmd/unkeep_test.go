package cmd

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestUnkeep(t *testing.T) {
	isCmdCalled := false
	isRootCalled := false
	app := New()

	app.unkeepCommand.Run = NewTracingHandler(&isCmdCalled)
	app.rootCommand.Run = NewTracingHandler(&isRootCalled)
	app.rootCommand.SetArgs([]string{"unkeep"})
	app.rootCommand.Execute()

	assert.True(t, isCmdCalled)
	assert.False(t, isRootCalled)
}
