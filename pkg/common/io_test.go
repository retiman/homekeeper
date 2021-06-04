package common

import (
	"fmt"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIsSymlink(t *testing.T) {
	if !IsSymlinkSupported || !IsLstatSupported {
		t.Skip("skipped because symlinks are not supported")
	}

	for _, symlink := range Fixtures.Symlinks {
		entry, err := os.Lstat(symlink)
		if err != nil {
			assert.Error(t, err)
			return
		}

		assert.True(t, IsSymlink(entry))
	}

	for _, file := range Fixtures.Files {
		entry, err := os.Stat(file)
		if err != nil {
			assert.Error(t, err)
			return
		}

		assert.False(t, IsSymlink(entry))
	}
}

func TestRemoveBrokenSymlinks(t *testing.T) {
	if !IsSymlinkSupported || !IsReadlinkSupported {
		t.Skip("skipped because symlinks are not supported")
	}

	defer UpdateDryRun(false)()
}

func TestListEntries(t *testing.T) {
	entries, err := ListEntries(Fixtures.RootDirectory)
	if err != nil {
		assert.Error(t, err)
		return
	}

	for _, entry := range entries {
		if entry.Name() == "dotfiles" {
			return
		}
	}

	assert.Error(t, fmt.Errorf("didn't find any 'dotfiles' directory: %+v", Fixtures))
}
