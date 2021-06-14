package common

import (
	"errors"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestKeepAndUnkeep(t *testing.T) {
	ctx := setupFixtures()
	checkSymlinkSupported(t)
	writeConfig(ctx, filepath.Join(ctx.HomeDirectory, ".homekeeper.yml"), ctx.Config)

	err := Keep(ctx)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	// Verify that each dotfiles directory has a corresponding symlink in the home directory, and that the symlink target
	// is in the dotfiles directory.
	for _, directory := range ctx.Config.Directories {
		log.Debugf("Checking for dotfiles symlinked from: %s", directory)
		entries, err := listEntries(fixtures.DotfilesDirectory)
		if err != nil {
			assert.Fail(t, err.Error())
		}

		for _, entry := range entries {
			symlink := filepath.Join(ctx.HomeDirectory, entry.Name())

			if ctx.Excludes[entry.Name()] == true {
				log.Debugf("Not checking excluded entry: %s", entry.Name())
				continue
			}

			log.Debugf("Checking that file/directory was symlinked: %s", entry.Name())
			entry, err = os.Lstat(symlink)
			if err != nil {
				assert.Fail(t, err.Error())
				continue
			}

			assert.True(t, isSymlink(entry), "Not a symlink: %+v", entry.Name())

			prefix := directory
			target, err := os.Readlink(symlink)
			if err != nil {
				assert.Fail(t, err.Error())
				continue
			}

			if runtime.GOOS == "windows" {
				prefix = strings.ToLower(prefix)
				target = strings.ToLower(target)
			}

			assert.True(t, strings.HasPrefix(target, prefix))
		}
	}

	err = Unkeep(ctx)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	// Verify that there are no symlinks in the home directory, then verify that every dotfiles directory has a
	// corresponding file/directory in the home directory.
	entries, err := listEntries(ctx.HomeDirectory)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	for _, entry := range entries {
		assert.False(t, isSymlink(entry))
	}

	for _, directory := range ctx.Config.Directories {
		log.Debugf("Checking for dotfiles symlinked from: %s", directory)
		entries, err := listEntries(fixtures.DotfilesDirectory)
		if err != nil {
			assert.Fail(t, err.Error())
		}

		for _, entry := range entries {
			if ctx.Excludes[entry.Name()] {
				log.Debugf("Skipping excluded entry: %s", entry.Name())
				continue
			}

			log.Debugf("Checking that file/directory was restored: %s", entry.Name())
			file := filepath.Join(ctx.HomeDirectory, entry.Name())
			_, err = os.Stat(file)
			if err != nil {
				assert.Fail(t, "File/directory '%s' doesn't exist: %+v", entry.Name(), err)
			}
		}
	}
}

func TestCleanup(t *testing.T) {
	ctx := setupFixtures()
	checkSymlinkSupported(t)
	writeConfig(ctx, filepath.Join(ctx.HomeDirectory, ".homekeeper.yml"), ctx.Config)

	err := Keep(ctx)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	err = os.RemoveAll(filepath.Join(ctx.Config.Directories[0], ".vimrc"))
	if err != nil {
		assert.Fail(t, err.Error())
	}

	err = Cleanup(ctx)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	_, err = os.Stat(filepath.Join(ctx.HomeDirectory, ".vimrc"))
	assert.True(t, errors.Is(err, os.ErrNotExist))
}
