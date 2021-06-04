package common

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestListEntries(t *testing.T) {
	paths, err := SetupFiles()
	if err != nil {
		return
	}

	entries, err := ListEntries(paths.RootDirectory)
	if err != nil {
		assert.Error(t, err)
		return
	}

	for _, entry := range entries {
		if entry.Name() == "dotfiles" {
			return
		}
	}

	assert.Error(t, fmt.Errorf("didn't find any 'dotfiles' directory: %+v", paths))
}
