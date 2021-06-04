package common

import (
	"fmt"
	"os"

	log "github.com/sirupsen/logrus"
)

func IsBrokenSymlink(entry os.FileInfo) bool {
	_, err := os.Readlink(entry.Name())
	if err != nil {
		return true
	}

	return false
}

func IsSymlink(entry os.FileInfo) bool {
	return entry.Mode()&os.ModeSymlink != 0
}

func ListEntries(directory string) (entries []os.FileInfo, err error) {
	fh, err := os.Open(directory)
	if err != nil {
		return
	}
	defer fh.Close()

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
	log.Tracef("checking for broken symlinks in: %s", directory)

	removedEntries = make([]string, 0)
	entries, err := ListEntries(directory)
	for _, entry := range entries {
		if !IsSymlink(entry) {
			log.Tracef("skipping non-symlink entry: %s", entry.Name())
			continue
		}

		if !IsBrokenSymlink(entry) {
			log.Tracef("skipping non-broken symlink entry: %s", entry.Name())
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
