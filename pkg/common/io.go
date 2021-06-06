package common

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
)

func CreateSymlink(oldname string, newname string, isOverwrite bool) (err error) {
	_, err = os.Stat(newname)
	if errors.Is(err, os.ErrExist) {
		if !isOverwrite {
			log.Warningf("will not overwrite existing file: %s", newname)
			return nil
		}

		log.Warningf("overwriting existing file: %s", newname)
		err = os.Remove(newname)
		if err != nil {
			return
		}
	}

	log.Infof("symlinking %s -> %s", oldname, newname)
	err = os.Symlink(oldname, newname)
	if err != nil {
		return
	}

	return
}

func CreateSymlinks(homeDirectory string, plan map[string]string) error {
	errs := make([]error, 0)
	for basename, oldname := range plan {
		newname := filepath.Join(homeDirectory, basename)
		err := CreateSymlink(oldname, newname, true /* isOverwrite */)
		if err != nil {
			errs = append(errs, err)
		}
	}

	if len(errs) != 0 {
		return fmt.Errorf("could not symlink some entries")
	}

	return nil
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
	log.Debugf("checking for broken symlinks in: %s", directory)

	removedEntries = make([]string, 0)
	entries, err := ListEntries(directory)
	for _, entry := range entries {
		path := filepath.Join(directory, entry.Name())

		if !IsSymlink(entry) {
			log.Debugf("skipping non-symlink entry: %s", path)
			continue
		}

		if !IsBrokenSymlink(entry) {
			log.Debugf("skipping non-broken symlink entry: %s", path)
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
