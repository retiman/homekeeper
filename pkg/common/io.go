package common

import (
	"fmt"
	"os"
	"path/filepath"

	log "github.com/sirupsen/logrus"
)

func CreateSymlinks(homeDirectory string, plan map[string]string) (err error) {
	errs := make([]error, 0)
	for basename, oldname := range plan {
		newname := filepath.Join(homeDirectory, basename)
		err := os.Symlink(oldname, newname)
		if err != nil {
			log.Warnf("could not symlink: %s -> %s", oldname, newname)
			errs = append(errs, err)
		} else {
			log.Infof("created symlink: %s -> %s", oldname, newname)
		}
	}

	if len(errs) == 0 {
		return fmt.Errorf("could not symlink some entries")
	}

	return
}

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
		err = fmt.Errorf("%s is not a directory", directory)
		return
	}

	// Read all entries.
	return fh.Readdir(-1)
}

func PlanSymlinks(homeDirectory string, dotfilesDirectory string, plan map[string]string) (err error) {
	entries, err := ListEntries(dotfilesDirectory)
	if err != nil {
		return err
	}

	for _, entry := range entries {
		plan[entry.Name()] = filepath.Join(dotfilesDirectory, entry.Name())
	}

	return
}

func RemoveBrokenSymlinks(directory string) (removedEntries []string, err error) {
	log.Tracef("checking for broken symlinks in: %s", directory)

	removedEntries = make([]string, 0)
	entries, err := ListEntries(directory)
	for _, entry := range entries {
		path := filepath.Join(directory, entry.Name())

		if !IsSymlink(entry) {
			log.Tracef("skipping non-symlink entry: %s", path)
			continue
		}

		if !IsBrokenSymlink(entry) {
			log.Tracef("skipping non-broken symlink entry: %s", path)
			continue
		}

		if IsDryRun {
			log.Infof("not removing broken symlink on dry run: %s", path)
			continue
		}

		log.Infof("removing broken symlink: %s", path)
		err = os.Remove(path)
		if err != nil {
			log.Errorf("could not remove broken symlink %s: %v", path, err)
			continue
		}

		removedEntries = append(removedEntries, path)
	}

	return
}
