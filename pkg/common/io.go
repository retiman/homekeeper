package common

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
)

func createSymlink(ctx *Context, source string, target string) (err error) {
	_, err = os.Stat(target)
	if errors.Is(err, os.ErrExist) {
		if !ctx.IsOverwrite {
			WriteOutput(ctx, "Skipping to avoid overwrite: %s", target)
			return nil
		}

		log.Warningf("Removing existing file: %s", target)
		err = os.Remove(target)
		if err != nil {
			return
		}
	}

	log.Infof("Symlinking file: %s", target)
	err = os.Symlink(source, target)
	if err != nil {
		return
	}

	return
}

func createSymlinks(ctx *Context, plan map[string]string) error {
	errs := make([]error, 0)
	for basename, source := range plan {
		target := filepath.Join(ctx.HomeDirectory, basename)
		err := createSymlink(ctx, source, target)
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
	return err != nil
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

	Infof, err := fh.Stat()
	if err != nil {
		return
	}

	if !Infof.Mode().IsDir() {
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
func planSymlinks(ctx *Context, dotfilesDirectory string, plan map[string]string) (err error) {
	entries, err := listEntries(dotfilesDirectory)
	if err != nil {
		return err
	}

	for _, entry := range entries {
		if ctx.Excludes[entry.Name()] {
			WriteOutput(ctx, "Ignoring file: %s", filepath.Join(dotfilesDirectory, entry.Name()))
			continue
		}

		plan[entry.Name()] = filepath.Join(dotfilesDirectory, entry.Name())
	}

	return
}

func removeBrokenSymlinks(ctx *Context, directory string) (removedEntries []string, err error) {
	log.Debugf("Checking for broken symlinks in: %s", directory)

	removedEntries = make([]string, 0)
	entries, err := listEntries(directory)
	for _, entry := range entries {
		path := filepath.Join(directory, entry.Name())

		if !isSymlink(entry) {
			log.Debugf("Skipping non-symlink entry: %s", path)
			continue
		}

		if !isBrokenSymlink(entry) {
			log.Debugf("Skipping non-broken symlink entry: %s", path)
			continue
		}

		if ctx.IsDryRun {
			WriteOutput(ctx, "Would remove broken symlink: %s", path)
			continue
		}

		WriteOutput(ctx, "Removing broken symlink: %s", path)
		err = os.Remove(path)
		if err != nil {
			WriteOutput(ctx, "Could not remove broken symlink: %s", path)
			continue
		}

		removedEntries = append(removedEntries, path)
	}

	return
}
