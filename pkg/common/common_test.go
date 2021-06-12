package common

import (
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"
)

type Fixtures struct {
	RootDirectory     string
	HomeDirectory     string
	DotfilesDirectory string
	Files             []string
	Directories       []string
	Symlinks          []string
}

var (
	// Even though Windows does support symlinks, by default, they are only available if the system administrator enables
	// them.  The rationale is that most applications are not written to support them, and enabling them by default would
	// present a security risk.
	isSymlinkSupported  bool
	isReadlinkSupported bool
	isLstatSupported    bool
	fixtures            *Fixtures
)

func init() {
	log = NewLogger("common", os.Stderr)
	IsDryRun = true
}

// Checks if symlink, lstat, and readlink are supported.  On all three major platforms (Linux, MacOS, and Windows),
// symlinks are supported.  However, by default, Windows does not have symlinks enabled.  It can only be enabled if
// the administrator enables them.  When on a platform where symlinks are not supported, the tests that require them
// should be skipped.
func checkSymlinkSupported(t *testing.T) {
	if !isSymlinkSupported {
		t.Skip("Skipping test because symlink not supported")
	}

	if !isLstatSupported {
		t.Skip("Skipping test because lstat not supported")
	}

	if !isReadlinkSupported {
		t.Skip("Skipping test because readlink not supported")
	}
}

// Gets the repository root of this project.  Temporary test files are stored in the "tmp" directory of the project
// root.  Rather than rely on relative paths hard-coded in tests based on the test directory, we try to find the
// repository root instead (this will stop programming errors like making a relative path to a directory that you
// wouldn't want to delete).
func getRepositoryRoot() (repositoryRoot string) {
	cwd, err := os.Getwd()
	if err != nil {
		panic(err)
	}

	repositoryRoot = cwd
	for {
		repositoryRoot = filepath.Join(repositoryRoot, "..")

		_, err = os.Stat(filepath.Join(repositoryRoot, ".git"))
		if err == nil {
			log.Debugf("Found repository root: %s", repositoryRoot)
			return
		}

		if errors.Is(err, os.ErrNotExist) {
			continue
		}

		if err != nil {
			panic(fmt.Errorf("Couldn't find repository root from %s: %v", cwd, err))
		}
	}
}

func setupFixtures() {
	IsDryRun = false
	fixtures = &Fixtures{}
	rootDirectory := getRepositoryRoot()

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
	log.Debugf("Removing all files from test directory: %s", fixtures.RootDirectory)
	err := os.RemoveAll(fixtures.RootDirectory)
	if err != nil {
		panic(err)
	}

	fixtures.Directories = createTestDirectories()
	fixtures.Files = createTestFiles()
	fixtures.Symlinks = createTestSymlinks()
}

func createTestDirectories() (directories []string) {
	directories = []string{
		fixtures.DotfilesDirectory,
		filepath.Join(fixtures.DotfilesDirectory, ".git"),
		filepath.Join(fixtures.DotfilesDirectory, ".vim"),
	}

	for _, directory := range directories {
		log.Debugf("Creating test directory: %s", directory)
		err := os.MkdirAll(directory, 0755)
		if err != nil {
			panic(err)
		}
	}

	return
}

func createTestFiles() (files []string) {
	files = []string{
		filepath.Join(fixtures.DotfilesDirectory, ".bash_profile"),
		filepath.Join(fixtures.DotfilesDirectory, ".gitconfig"),
		filepath.Join(fixtures.DotfilesDirectory, ".gitignore"),
		filepath.Join(fixtures.DotfilesDirectory, ".vimrc"),
		filepath.Join(fixtures.DotfilesDirectory, "README.md"),
	}

	for _, file := range files {
		log.Debugf("Creating test file: %s", file)
		fh, err := os.Create(file)
		if err != nil {
			panic(err)
		}
		defer fh.Close()
	}

	return
}

func createTestSymlinks() (symlinks []string) {
	isSymlinkSupported = false
	isReadlinkSupported = false
	isLstatSupported = false

	source := filepath.Join(fixtures.DotfilesDirectory, ".bash_profile")
	target := filepath.Join(fixtures.DotfilesDirectory, ".bashrc")
	symlinks = []string{target}

	log.Debugf("Attempting to symlinking %s -> %s", source, target)
	err := os.Symlink(source, target)
	if err != nil {
		log.Warningf("Symlink is not supported on this system: %+v", err)

		// There's no point in checking for readlink or lstat if the symlink creation fails.  If it succeeds, we can check
		// and see if either will succeed if the other fails.
		return
	} else {
		isSymlinkSupported = true
	}

	_, err = os.Readlink(target)
	if err != nil {
		log.Warningf("Readlink is not supported on this system: %v", err)
	} else {
		isReadlinkSupported = true
	}

	_, err = os.Lstat(target)
	if err != nil {
		log.Warningf("Lstat is not supported on this system: %v", err)
	} else {
		isLstatSupported = true
	}

	return
}

func readFileAsString(file string) string {
	content, err := ioutil.ReadFile(file)
	if err != nil {
		panic(err)
	}

	return string(content)
}
