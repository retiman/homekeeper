package common

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"

	"github.com/retiman/homekeeper/pkg/log"
)

func createSymlink(source string, target string, isOverwrite bool) (err error) {
	_, err = os.Stat(target)
	if errors.Is(err, os.ErrExist) {
		if !isOverwrite {
			log.Warnf("will not overwrite existing file: %s", target)
			return nil
		}

		log.Warnf("overwriting existing file: %s", target)
		err = os.Remove(target)
		if err != nil {
			return
		}
	}

	log.Infof("symlinking %s -> %s", source, target)
	err = os.Symlink(source, target)
	if err != nil {
		return
	}

	return
}

func createSymlinks(homeDirectory string, plan map[string]string) error {
	errs := make([]error, 0)
	for basename, source := range plan {
		target := filepath.Join(homeDirectory, basename)
		err := createSymlink(source, target, true /* isOverwrite */)
		if err != nil {
			errs = append(errs, err)
		}
	}

	if len(errs) != 0 {
		return fmt.Errorf("could not symlink some entries")
	}

	return nil
}

func isBrokenSymlink(entry os.FileInfo) bool {
	_, err := os.Readlink(entry.Name())
	if err != nil {
		return true
	}

	return false
}

func isSymlink(entry os.FileInfo) bool {
	return entry.Mode()&os.ModeSymlink != 0
}

func listEntries(directory string) (entries []os.FileInfo, err error) {
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

// Makes a plan of symlinks based on an existing one.  With an empty plan, makes a plan of all dotfiles to the home
// directory.  When there are multiple dotfiles directories, call this function multiple times, updating the plan each
// time.
//
// Pass in a set of files to filter out (such as .git, .gitignore, README.md, etc) to exclude them from the plan.
func planSymlinks(homeDirectory string, dotfilesDirectory string, plan map[string]string, excludes map[string]bool) (err error) {
	entries, err := listEntries(dotfilesDirectory)
	if err != nil {
		return err
	}

	for _, entry := range entries {
		if excludes[entry.Name()] {
			log.Debugf("excluding from symlinking: %s", entry.Name())
			continue
		}

		plan[entry.Name()] = filepath.Join(dotfilesDirectory, entry.Name())
	}

	return
}

func removeBrokenSymlinks(directory string) (removedEntries []string, err error) {
	log.Debugf("checking for broken symlinks in: %s", directory)

	removedEntries = make([]string, 0)
	entries, err := listEntries(directory)
	for _, entry := range entries {
		path := filepath.Join(directory, entry.Name())

		if !isSymlink(entry) {
			log.Debugf("skipping non-symlink entry: %s", path)
			continue
		}

		if !isBrokenSymlink(entry) {
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
