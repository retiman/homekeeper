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
	setupFixtures()
	checkSymlinkSupported(t)

	plan := make(map[string]string)
	err := planSymlinks(fixtures.HomeDirectory, fixtures.DotfilesDirectory, plan, make(map[string]bool))
	if err != nil {
		assert.Fail(t, err.Error())
	}

	err = createSymlinks(fixtures.HomeDirectory, plan)
	if err != nil {
		assert.Fail(t, err.Error())
	}
}

func TestIsSymlink(t *testing.T) {
	setupFixtures()
	checkSymlinkSupported(t)

	for _, symlink := range fixtures.Symlinks {
		entry, err := os.Lstat(symlink)
		if err != nil {
			assert.Fail(t, err.Error())
			return
		}

		assert.True(t, isSymlink(entry))
	}

	for _, file := range fixtures.Files {
		entry, err := os.Stat(file)
		if err != nil {
			assert.Fail(t, err.Error())
			return
		}

		assert.False(t, isSymlink(entry))
	}
}

func TestRemoveBrokenSymlinks(t *testing.T) {
	setupFixtures()
	checkSymlinkSupported(t)

	expected := make([]string, 0)
	for _, target := range fixtures.Symlinks {
		source, err := os.Readlink(target)
		if err != nil {
			assert.Fail(t, err.Error())
		}

		log.Debugf("creating a broken symlink; removing: %s", source)
		os.Remove(source)
		expected = append(expected, target)
	}

	actual, err := removeBrokenSymlinks(fixtures.DotfilesDirectory)
	if err != nil {
		assert.Fail(t, err.Error())
		return
	}

	assert.ElementsMatch(t, actual, expected)
}

func TestListEntries(t *testing.T) {
	setupFixtures()

	entries, err := listEntries(fixtures.HomeDirectory)
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

	assert.Fail(t, fmt.Sprintf("didn't find any 'dotfiles' directory: %+v", fixtures))
}

func TestPlanSymlinks(t *testing.T) {
	setupFixtures()

	excludes := make(map[string]bool)
	excludes[".gitignore"] = true
	excludes["README.md"] = true

	plan := make(map[string]string)
	err := planSymlinks(fixtures.HomeDirectory, fixtures.DotfilesDirectory, plan, excludes)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	entries, err := listEntries(fixtures.DotfilesDirectory)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	actual := len(plan)
	expected := len(entries) - len(excludes)
	assert.Equal(t, actual, expected)
	for basename, target := range plan {
		assert.True(t, strings.HasPrefix(target, fixtures.DotfilesDirectory))
		assert.False(t, strings.Contains(basename, string(os.PathSeparator)))
	}
}
