package common

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"

	log "github.com/sirupsen/logrus"
)

var (
	// Even though Windows does support symlinks, by default, they are only available if the system administrator enables
	// them.  The rationale is that most applications are not written to support them, and enabling them by default would
	// present a security risk.
	IsSymlinkSupported bool
	IsReadlinkSupported bool
	IsLstatSupported bool
)

type Paths struct {
	RootDirectory     string
	HomeDirectory     string
	DotfilesDirectory string
}

func init() {
	log.SetFormatter(&log.TextFormatter{
		DisableTimestamp: true,
		PadLevelText:     true,
		QuoteEmptyFields: true,
		DisableQuote:     true,
	})

	log.SetLevel(log.DebugLevel)
}

func GetRepositoryRoot() (repositoryRoot string, err error) {
	cwd, err := os.Getwd()
	if err != nil {
		return
	}

	repositoryRoot = cwd
	for {
		repositoryRoot = filepath.Join(repositoryRoot, "..")

		_, err = os.Stat(filepath.Join(repositoryRoot, ".git"))
		if err == nil {
			log.Tracef("found repository root: %s", repositoryRoot)
			return
		}

		if errors.Is(err, os.ErrNotExist) {
			continue
		}

		if err != nil {
			err = fmt.Errorf("couldn't find repository root from %s: %v", cwd, err)
			return
		}
	}
}

func SetupFiles() (paths *Paths, err error) {
	paths = &Paths{}
	rootDirectory, err := GetRepositoryRoot()
	if err != nil {
		return
	}

	// It's okay to use this path as the root directory tests in golang; all tests run sequentially unless you explicitly
	// mark them for parallel execution.
	paths.RootDirectory = filepath.Join(rootDirectory, "tmp")
	paths.HomeDirectory = filepath.Join(paths.RootDirectory, "home", "johndoe")
	paths.DotfilesDirectory = filepath.Join(paths.HomeDirectory, "dotfiles")

	// We could use something like afero's in-memory FS for this, but we do want to test out functionality in different
	// platforms.  There is some argument to running the in-memory tests first, before running them on the real filesystem
	// (just in case you messed up and put the wrong directory here, you could clear out a directory on your dev machine
	// you didn't intend to, but the GetRepositoryRoot() method should prevent you from doing that).
	//
	// This way we can test out different platforms as well.
	log.Tracef("removing all files in directory: %s", paths.RootDirectory)
	err = os.RemoveAll(paths.RootDirectory)
	if err != nil {
		return
	}

	_, err = CreateTestDirectories(paths)
	if err != nil {
		return
	}

	_, err = CreateTestFiles(paths)
	if err != nil {
		return
	}

	_, err = CreateTestSymlinks(paths)
	if err != nil {
		return
	}

	return
}

func CreateTestDirectories(paths *Paths) (directories []string, err error) {
	directories = []string{
		paths.DotfilesDirectory,
		filepath.Join(paths.DotfilesDirectory, ".git"),
		filepath.Join(paths.DotfilesDirectory, ".vim"),
	}

	for _, directory := range directories {
		log.Tracef("creating test directory: %s", directory)
		err = os.MkdirAll(directory, os.ModePerm)
		if err != nil {
			return
		}
	}

	return
}

func CreateTestFiles(paths *Paths) (files []string, err error) {
	files = []string{
		filepath.Join(paths.DotfilesDirectory, ".bash_profile"),
		filepath.Join(paths.DotfilesDirectory, ".gitconfig"),
		filepath.Join(paths.DotfilesDirectory, ".vimrc"),
	}

	for _, file := range files {
		log.Tracef("creating test file: %s", file)
		_, err = os.Create(file)
		if err != nil {
			return
		}
	}

	return
}

func CreateTestSymlinks(paths *Paths) (symlinks []string, err error) {
	source := filepath.Join(paths.DotfilesDirectory, ".bash_profile")
	target := filepath.Join(paths.DotfilesDirectory, ".bashrc")
	symlinks = []string{target}

	log.Tracef("symlinking %s -> %s", source, target)
	err = os.Symlink(source, target)
	if err != nil {
		IsSymlinkSupported = false
		log.Warnf("symlink is not supported on this system: %+v", err)
		return
	}

	_, err = os.Readlink(target)
	if err != nil {
		IsReadlinkSupported = false
		log.Warnf("readlink is not supported on this system: %+v", err)
	}

	_, err = os.Lstat(target)
	if err != nil {
		IsLstatSupported = false
		log.Warnf("lstat is not supported on this system: %+v", err)
	}

	err = nil
	return
}
