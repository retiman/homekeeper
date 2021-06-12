package common

import (
	"os"
	"path/filepath"
	"runtime"
	"strings"
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

	entries, err := listEntries(fixtures.DotfilesDirectory)
	if err != nil {
		assert.Fail(t, err.Error())
	}
	for _, entry := range entries {
		newname := filepath.Join(fixtures.HomeDirectory, entry.Name())
		assert.True(t, isSymlink(entry), "Not a symlink: %+v", newname)

		prefix := fixtures.DotfilesDirectory
		oldname, err := os.Readlink(newname)
		if err != nil {
			assert.Fail(t, err.Error())
		}

		// Windows filenames are not case sensitive, and filepath.HasPrefix doesn't properly consider lowercasing.  Dirty
		// hack to make things work on windows.
		if runtime.GOOS == "windows" {
			prefix = strings.ToLower(prefix)
			oldname = strings.ToLower(prefix)
		}

		assert.True(t, strings.HasPrefix(oldname, prefix))
	}
}

func TestUnkeep(t *testing.T) {
}

func TestCleanup(t *testing.T) {
}
