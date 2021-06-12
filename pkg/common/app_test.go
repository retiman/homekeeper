package common

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestKeep(t *testing.T) {
	ctx := setupFixtures()
	checkSymlinkSupported(t)
	writeConfig(ctx, filepath.Join(ctx.HomeDirectory, ".homekeeper.yml"), ctx.Config)

	err := Keep(ctx)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	for _, directory := range ctx.Config.Directories {
		log.Debugf("Checking for dotfiles symlinked from: %s", directory)
		entries, err := listEntries(fixtures.DotfilesDirectory)
		if err != nil {
			assert.Fail(t, err.Error())
		}

		for _, entry := range entries {
			if ctx.Excludes[entry.Name()] == true {
				log.Debugf("Not checking excluded entry: %s", entry.Name())
				continue
			}

			log.Debugf("Checking that file/directory was symlinked: %s", entry.Name())
			entry, err = os.Lstat(filepath.Join(ctx.HomeDirectory, entry.Name()))
			if err != nil {
				assert.Fail(t, err.Error())
				continue
			}

			assert.True(t, isSymlink(entry), "Not a symlink: %+v", entry.Name())
		}
	}
}

func TestUnkeep(t *testing.T) {
	ctx := setupFixtures()
	checkSymlinkSupported(t)
	writeConfig(ctx, filepath.Join(ctx.HomeDirectory, ".homekeeper.yml"), ctx.Config)

	err := Keep(ctx)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	err = Unkeep(ctx)
	if err != nil {
		assert.Fail(t, err.Error())
	}
}

func TestCleanup(t *testing.T) {
	ctx := setupFixtures()
	checkSymlinkSupported(t)
	writeConfig(ctx, filepath.Join(ctx.HomeDirectory, ".homekeeper.yml"), ctx.Config)

}
