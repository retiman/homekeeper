package common

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"testing"

	log "github.com/sirupsen/logrus"
)

var (
	// Even though Windows does support symlinks, by default, they are only available if the system administrator enables
	// them.  The rationale is that most applications are not written to support them, and enabling them by default would
	// present a security risk.
	IsSymlinkSupported  bool
	IsReadlinkSupported bool
	IsLstatSupported    bool
	Fixtures            *TestFixtures
)

type TestFixtures struct {
	RootDirectory     string
	HomeDirectory     string
	DotfilesDirectory string
	Files             []string
	Directories       []string
	Symlinks          []string
}

func init() {
	IsDryRun = true

	log.SetFormatter(&log.TextFormatter{
		DisableTimestamp: true,
		PadLevelText:     true,
		QuoteEmptyFields: true,
		DisableQuote:     true,
	})

	log.SetLevel(log.TraceLevel)
}

func TestMain(t *testing.M) {
	var err error
	Fixtures, err = SetupFixtures()
	if err != nil {
		log.Errorf("error during test setup: %v", err)
		os.Exit(1)
	}

	code := t.Run()
	os.Exit(code)
}

func CheckSymlink(t *testing.T) {
	if !IsSymlinkSupported {
		t.Skip("skipping test because symlink not supported")
	}

	if !IsLstatSupported {
		t.Skip("skipping test because lstat not supported")
	}

	if !IsReadlinkSupported {
		t.Skip("skipping test because readlink not supported")
	}
}

func UpdateDryRun(value bool) func() {
	if IsDryRun == value {
		return func() {}
	}

	log.Tracef("setting dry run value: %v", value)
	previousValue := IsDryRun
	IsDryRun = value
	return func() {
		log.Tracef("restoring dry run value: %v", previousValue)
		IsDryRun = previousValue
	}
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

func SetupFixtures() (fixtures *TestFixtures, err error) {
	fixtures = &TestFixtures{}
	rootDirectory, err := GetRepositoryRoot()
	if err != nil {
		return
	}

	// It's okay to use this path as the root directory tests in golang; all tests run sequentially unless you explicitly
	// mark them for parallel execution.
	fixtures.RootDirectory = filepath.Join(rootDirectory, "tmp")
	fixtures.HomeDirectory = filepath.Join(fixtures.RootDirectory, "home", "johndoe")
	fixtures.DotfilesDirectory = filepath.Join(fixtures.HomeDirectory, "dotfiles")

	// We could use something like afero's in-memory FS for this, but we do want to test out functionality in different
	// platforms.  There is some argument to running the in-memory tests first, before running them on the real filesystem
	// (just in case you messed up and put the wrong directory here, you could clear out a directory on your dev machine
	// you didn't intend to, but the GetRepositoryRoot() method should prevent you from doing that).
	//
	// This way we can test out different platforms as well.
	log.Tracef("removing all files in directory: %s", fixtures.RootDirectory)
	err = os.RemoveAll(fixtures.RootDirectory)
	if err != nil {
		return
	}

	fixtures.Directories, err = CreateTestDirectories(fixtures)
	if err != nil {
		return
	}

	fixtures.Files, err = CreateTestFiles(fixtures)
	if err != nil {
		return
	}

	fixtures.Symlinks = CreateTestSymlinks(fixtures)
	return
}

func CreateTestDirectories(fixtures *TestFixtures) (directories []string, err error) {
	directories = []string{
		fixtures.DotfilesDirectory,
		filepath.Join(fixtures.DotfilesDirectory, ".git"),
		filepath.Join(fixtures.DotfilesDirectory, ".vim"),
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

func CreateTestFiles(fixtures *TestFixtures) (files []string, err error) {
	files = []string{
		filepath.Join(fixtures.DotfilesDirectory, ".bash_profile"),
		filepath.Join(fixtures.DotfilesDirectory, ".gitconfig"),
		filepath.Join(fixtures.DotfilesDirectory, ".vimrc"),
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

func CreateTestSymlinks(fixtures *TestFixtures) (symlinks []string) {
	oldname := filepath.Join(fixtures.DotfilesDirectory, ".bash_profile")
	newname := filepath.Join(fixtures.DotfilesDirectory, ".bashrc")
	symlinks = []string{newname}

	log.Tracef("symlinking %s -> %s", oldname, newname)
	err := os.Symlink(oldname, newname)
	if err != nil {
		IsSymlinkSupported = false
		log.Warnf("symlink is not supported on this system: %+v", err)

		// There's no point in checking for readlink or lstat if the symlink creation fails.  If it succeeds, we can check
		// and see if either will succeed if the other fails.
		return
	} else {
		IsSymlinkSupported = true
	}

	_, err = os.Readlink(newname)
	if err != nil {
		IsReadlinkSupported = false
		log.Warnf("readlink is not supported on this system: %v", err)
		err = nil
	} else {
		IsReadlinkSupported = true
	}

	_, err = os.Lstat(newname)
	if err != nil {
		IsLstatSupported = false
		log.Warnf("lstat is not supported on this system: %v", err)
		err = nil
	} else {
		IsLstatSupported = true
	}

	return
}
