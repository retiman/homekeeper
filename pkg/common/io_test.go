package common

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	log "github.com/sirupsen/logrus"
	"github.com/stretchr/testify/assert"
)

func TestCreateSymlinks(t *testing.T) {
}

func TestIsSymlink(t *testing.T) {
	if !IsSymlinkSupported || !IsLstatSupported {
		t.Skip("skipped because symlinks are not supported")
	}

	for _, symlink := range Fixtures.Symlinks {
		entry, err := os.Lstat(symlink)
		if err != nil {
			assert.Fail(t, err.Error())
			return
		}

		assert.True(t, IsSymlink(entry))
	}

	for _, file := range Fixtures.Files {
		entry, err := os.Stat(file)
		if err != nil {
			assert.Fail(t, err.Error())
			return
		}

		assert.False(t, IsSymlink(entry))
	}
}

func TestRemoveBrokenSymlinks(t *testing.T) {
	if !IsSymlinkSupported || !IsReadlinkSupported {
		t.Skip("skipped because symlinks are not supported")
		return
	}

	defer UpdateDryRun(false)()

	wanted := make([]string, 0)
	for _, symlink := range Fixtures.Symlinks {
		oldname, err := os.Readlink(symlink)
		if err != nil {
			assert.Fail(t, err.Error())
		}

		log.Tracef("creating a broken symlink; removing: %s", oldname)
		os.Remove(oldname)
		wanted = append(wanted, symlink)
	}

	got, err := RemoveBrokenSymlinks(Fixtures.DotfilesDirectory)
	if err != nil {
		assert.Fail(t, err.Error())
		return
	}

	assert.ElementsMatch(t, got, wanted)
}

func TestListEntries(t *testing.T) {
	entries, err := ListEntries(Fixtures.HomeDirectory)
	if err != nil {
		assert.Fail(t, err.Error())
		return
	}

	for _, entry := range entries {
		parts := filepath.SplitList(entry.Name())
		if len(parts) == 0 {
			continue
		}

		if parts[len(parts)-1] == "dotfiles" {
			return
		}
	}

	assert.Fail(t, fmt.Sprintf("didn't find any 'dotfiles' directory: %+v", Fixtures))
}

func TestPlanSymlinks(t *testing.T) {
	plan := make(map[string]string)
	PlanSymlinks(Fixtures.HomeDirectory, Fixtures.DotfilesDirectory, plan)

	entries, err := ListEntries(Fixtures.DotfilesDirectory)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	assert.Equal(t, len(plan), len(entries))
	for basename, newname := range plan {
		assert.True(t, strings.HasPrefix(newname, Fixtures.DotfilesDirectory))
		assert.False(t, strings.Contains(basename, string(os.PathSeparator)))
	}
}
