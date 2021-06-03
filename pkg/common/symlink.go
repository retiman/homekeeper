package common

import (
	"errors"
	"fmt"
	"os"
	"runtime"

	log "github.com/sirupsen/logrus"
)

func (app *App) createOrCopySymlink(source string, target string) (err error) {
	// On Windows, creating a symlink requires Administrator privileges because
	// enabling them can expose security vulnerabilities in applications that
	// weren't designed to expect them.
	// https://security.stackexchange.com/questions/10194/why-do-you-have-to-be-an-admin-to-create-a-symlink-in-windows
	if runtime.GOOS != "windows" {
		return os.Symlink(source, target)
	}

}

func (app *App) isBrokenSymlink(entry os.FileInfo) (isBroken bool, err error) {
	isBroken = false
	if !app.isSymlink(entry) {
		return
	}

	log.Tracef("entry is symlink; checking if broken: %s", entry.Name())
	target, err := os.Readlink(entry.Name())
	if err != nil {
		err = fmt.Errorf("couldn't read symlink %s: %v", entry.Name(), err)
		return
	}

	_, err = os.Stat(target)
	if err == nil {
		log.Tracef("symlink is not broken; skipping: %s", entry.Name())
		return
	}

	if !errors.Is(err, os.ErrNotExist) {
		err = fmt.Errorf("couldn't stat file %s: %v", entry.Name(), err)
		return
	}

	isBroken = true
	return
}

func (app *App) isSymlink(entry os.FileInfo) bool {
	return entry.Mode()&os.ModeSymlink != 0
}

func (app *App) removeBrokenSymlinks(directory string) (err error) {
	entries, err := app.listEntries(directory)
	for _, entry := range entries {
		if err = app.removeBrokenSymlink(entry); err != nil {
			return
		}
	}

	return
}

func (app *App) removeBrokenSymlink(entry os.FileInfo) (err error) {
	isBroken, err := app.isBrokenSymlink(entry)
	if err != nil {
		return
	}

	if !isBroken {
		return
	}

	if app.IsDryRun {
		fmt.Printf("not removing broken symlink in dry run: %s", entry.Name())
		return
	}

	err = os.Remove(entry.Name())
	if err != nil {
		return fmt.Errorf("couldn't remove broken symlink %s: %v", entry.Name(), err)
	}

	fmt.Printf("removed broken symlink: %s", entry.Name())
	return
}
