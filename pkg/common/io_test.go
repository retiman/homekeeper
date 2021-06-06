package common

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCreateSymlinks(t *testing.T) {
	CheckSymlinkSupported(t)
	defer UpdateDryRun(false)()

	plan := make(map[string]string)
	err := PlanSymlinks(Fixtures.HomeDirectory, Fixtures.DotfilesDirectory, plan, make(map[string]bool))
	if err != nil {
		assert.Fail(t, err.Error())
	}

	err = CreateSymlinks(Fixtures.HomeDirectory, plan)
	if err != nil {
		assert.Fail(t, err.Error())
	}
}

func TestIsSymlink(t *testing.T) {
	CheckSymlinkSupported(t)

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
	CheckSymlinkSupported(t)
	defer UpdateDryRun(false)()

	wanted := make([]string, 0)
	for _, symlink := range Fixtures.Symlinks {
		oldname, err := os.Readlink(symlink)
		if err != nil {
			assert.Fail(t, err.Error())
		}

		log.Debugf("creating a broken symlink; removing: %s", oldname)
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
	excludes := make(map[string]bool)
	excludes[".gitignore"] = true
	excludes["README.md"] = true

	plan := make(map[string]string)
	err := PlanSymlinks(Fixtures.HomeDirectory, Fixtures.DotfilesDirectory, plan, excludes)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	entries, err := ListEntries(Fixtures.DotfilesDirectory)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	actual := len(plan)
	expected := len(entries) - len(excludes)
	assert.Equal(t, actual, expected)
	for basename, target := range plan {
		assert.True(t, strings.HasPrefix(target, Fixtures.DotfilesDirectory))
		assert.False(t, strings.Contains(basename, string(os.PathSeparator)))
	}
}
