package common

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/otiai10/copy"
)

func createSymlink(ctx *Context, oldname string, newname string) (err error) {
	_, err = os.Stat(oldname)
	if errors.Is(err, os.ErrExist) {
		if ctx.IsNoOverwrite {
			Writeln(ctx, "Skipping because file would be overwritten: %s", newname)
			err = nil
			return
		}

		log.Warningf("Removing existing file: %s", newname)
		err = os.RemoveAll(newname)
		if err != nil {
			Writeln(ctx, "Skipping because file couldn't be removed: %s", newname)
			log.Errorf("Could not remove file: %+v", err)
			return
		}
	}

	err = os.Symlink(oldname, newname)
	if err != nil {
		Writeln(ctx, "Skipping because file couldn't be symlinked: %s", newname)
		log.Errorf("Could not create symlink: %+v", err)
		return
	}

	Writeln(ctx, "Symlinked file: %s -> %s", oldname, newname)
	return
}

func createSymlinks(ctx *Context, plan map[string]string) (err error) {
	for basename, oldname := range plan {
		newname := filepath.Join(ctx.HomeDirectory, basename)
		err := createSymlink(ctx, oldname, newname)
		if err != nil {
			continue
		}
	}

	if err != nil {
		err = fmt.Errorf("could not symlink some entries")
	}

	return
}

func isBrokenSymlink(file string) bool {
	target, err := os.Readlink(file)
	if err != nil {
		return true
	}

	_, err = os.Stat(target)
	if err == nil {
		return false
	}

	if errors.Is(err, os.ErrNotExist) {
		return true
	}

	if errors.Is(err, os.ErrExist) {
		return false
	}

	// Schrodinger's symlink.  It wasn't reported as existing or not existing, but we'll assume it doesn't so it doesn't
	// become inadvertently removed.
	log.Warningf("Couldn't determine if file/directory exists (assuming not broken): %s", target)
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
		err = fmt.Errorf("not a directory")
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
	log.Debugf("Planning symlinks from directory: %s", dotfilesDirectory)
	entries, err := listEntries(dotfilesDirectory)
	if err != nil {
		return
	}

	for _, entry := range entries {
		if ctx.Excludes[entry.Name()] {
			Writeln(ctx, "Ignoring file: %s", filepath.Join(dotfilesDirectory, entry.Name()))
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

		if !isBrokenSymlink(path) {
			log.Debugf("Skipping non-broken symlink entry: %s", path)
			continue
		}

		if ctx.IsDryRun {
			Writeln(ctx, "Would remove broken symlink: %s", path)
			continue
		}

		Writeln(ctx, "Removing broken symlink: %s", path)
		err = os.Remove(path)
		if err != nil {
			Writeln(ctx, "Could not remove broken symlink: %s", path)
			continue
		}

		removedEntries = append(removedEntries, path)
	}

	return
}

func restoreSymlinks(ctx *Context) (err error) {
	log.Debugf("Restoring symlinks in home directory: %s", ctx.HomeDirectory)
	entries, err := listEntries(ctx.HomeDirectory)
	if err != nil {
		return
	}

	for _, entry := range entries {
		if !isSymlink(entry) {
			log.Debugf("Skipping non-symlink entry: %s", entry.Name())
			continue
		}

		symlink := filepath.Join(ctx.HomeDirectory, entry.Name())
		target, err := os.Readlink(symlink)
		if err != nil {
			log.Warningf("Skipping because could not readlink: %s", entry.Name())
			continue
		}

		for _, prefix := range ctx.Config.Directories {
			target, err = filepath.Abs(target)
			if err != nil {
				log.Warningf("Skipping because could not determine absolute path: %s", target)
				continue
			}

			// On Windows, filesystem paths are not case sensitive, so we lowercase them before comparison first.
			if runtime.GOOS == "windows" {
				log.Infof("Lowercasing filename on windows: %s", prefix)
				prefix = strings.ToLower(prefix)

				log.Infof("Lowercasing filename on windows: %s", target)
				target = strings.ToLower(target)
			}

			// The filepath.HasPrefix() method is deprecated and should not be used as it does not properly detect situations
			// where case matters.
			if !strings.HasPrefix(target, prefix) {
				log.Debugf("Skipping because readlink target is not in a dotfiles directory: %s", target)
				continue
			}

			oldname := target
			newname := symlink
			err = restoreSymlink(ctx, oldname, newname)
			if err != nil {
				continue
			}
		}
	}

	if err != nil {
		log.Errorf("Some symlinks could not be restored.")
	}

	return
}

func restoreSymlink(ctx *Context, oldname string, newname string) (err error) {
	log.Debugf("Removing existing file: %s", newname)
	if !ctx.IsDryRun {
		err = os.RemoveAll(newname)
		if err != nil {
			Writeln(ctx, "Skipping because file couldn't be removed: %s", newname)
			log.Errorf("Could not remove file: %+v", err)
			return
		}
	} else {
		Writeln(ctx, "Would have removed file: %s", newname)
	}

	if !ctx.IsDryRun {
		err = copy.Copy(oldname, newname)
		if err != nil {
			Writeln(ctx, "Skipping because file couldn't be copied:", oldname)
			log.Errorf("Could not copy file/directory: %+v", err)
			return
		}

		Writeln(ctx, "Restored file: %s <- %s", newname, oldname)
	} else {
		Writeln(ctx, "Would have restored file: %s <- %s", newname, oldname)
	}

	return
}
