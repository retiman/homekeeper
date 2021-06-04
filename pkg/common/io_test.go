package common

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIsSymlink(t *testing.T) {
	if !IsSymlinkSupported {
		t.Skip("skipped because symlinks are not supported")
	}
}

func TestListEntries(t *testing.T) {
	entries, err := ListEntries(TestPaths.RootDirectory)
	if err != nil {
		assert.Error(t, err)
		return
	}

	for _, entry := range entries {
		if entry.Name() == "dotfiles" {
			return
		}
	}

	assert.Error(t, fmt.Errorf("didn't find any 'dotfiles' directory: %+v", TestPaths))
}
