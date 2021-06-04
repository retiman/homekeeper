package common

import (
	"errors"
	"fmt"
	"os"

	log "github.com/sirupsen/logrus"
)

func IsBrokenSymlink(entry os.FileInfo) (isBroken bool, err error) {
	isBroken = false
	if IsSymlink(entry) {
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

func IsSymlink(entry os.FileInfo) bool {
	return entry.Mode()&os.ModeSymlink != 0
}

func ListEntries(directory string) (entries []os.FileInfo, err error) {
	fh, err := os.Open(directory)
	defer fh.Close()
	if err != nil {
		return
	}

	info, err := fh.Stat()
	if err != nil {
		return
	}

	if !info.Mode().IsDir() {
		err = fmt.Errorf("not a directory: %s", directory)
		return
	}

	// Read all entries.
	return fh.Readdir(-1)
}

func RemoveBrokenSymlinks(directory string) (removedEntries []string, err error) {
	removedEntries = make([]string, 0)
	entries, err := ListEntries(directory)
	for _, entry := range entries {
		if !IsSymlink(entry) {
			log.Tracef("skipping non-symlink entry: %s", entry.Name())
			continue
		}

		if IsDryRun {
			log.Infof("not removing broken symlink on dry run: %s", entry.Name())
			continue
		}

		err = os.Remove(entry.Name())
		if err != nil {
			log.Errorf("could not remove broken symlink %s: %v", entry.Name(), err)
			continue
		}

		log.Infof("removed broken symlink: %s", entry.Name())
		removedEntries = append(removedEntries, entry.Name())
	}

	return
}
