package common

import (
	"fmt"
	"os"
	path "path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	log "github.com/sirupsen/logrus"
)

func TestRemoveBrokenSymlinks(t *testing.T) {
	paths := SetupBrokenSymlinks(t)
	app := &App{IsDryRun: true}
	err := app.removeBrokenSymlinks(paths.HomeDirectory)
	if err != nil {
		assert.Fail(t, err.Error())
	}
}

func SetupBrokenSymlinks(t *testing.T) (paths *Paths) {
	paths, err := SetupFiles()
	if err != nil {
		assert.Fail(t, err.Error())
	}

	for i := 0; i < 10; i++ {
		name := fmt.Sprintf("broken%d.txt", i)
		source := path.Join(paths.RootDirectory, name)
		target := path.Join(paths.HomeDirectory, name)

		log.Debugf("creating broken symlink (%s): %s", source, target)
		err = os.Symlink(source, target)
		if err != nil {
			assert.Fail(t, err.Error())
		}
	}

	return
}
