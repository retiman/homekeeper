package common

import (
	"fmt"
	"os"
	"path/filepath"

	log "github.com/sirupsen/logrus"
)

type Paths struct {
	RootDirectory string
	HomeDirectory string
	DotfilesDirectory string
}

func init() {
	log.SetFormatter(&log.TextFormatter{
		DisableTimestamp: true,
		PadLevelText:     true,
		QuoteEmptyFields: true,
		DisableQuote:     true,
	})

	log.SetLevel(log.TraceLevel)
}

func GetRepositoryRoot() (path string, err error) {
	cwd, err := os.Getwd()
	if err != nil {
		return
	}

	path = cwd
	for {
		path = filepath.Join(path, "..")

		_, err = os.Stat(filepath.Join(path, ".git"))
		if os.IsExist(err) {
			log.Debugf("found repository root: %s", path)
			return
		}

		if !os.IsNotExist(err) {
			err = fmt.Errorf("couldn't find repository root from: %s", cwd)
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

	paths.RootDirectory = filepath.Join(rootDirectory, "tmp")
	paths.HomeDirectory = filepath.Join(paths.RootDirectory, "home", "johndoe")
	paths.DotfilesDirectory = filepath.Join(paths.HomeDirectory, "dotfiles")

	log.Debugf("setting test directory to: %s", paths.RootDirectory)
	_, err = os.Stat(filepath.Join(paths.RootDirectory, ".git"))
	if os.IsNotExist(err) {
		err = fmt.Errorf("couldn't find the .git directory; do")
		return
	}

	log.Debugf("removing all files in directory: %s", paths.RootDirectory)
	err = os.RemoveAll(paths.RootDirectory)
	if err != nil {
		return
	}

	directories := []string{
		paths.DotfilesDirectory,
		filepath.Join(paths.DotfilesDirectory, ".git"),
		filepath.Join(paths.DotfilesDirectory, ".vim"),
	}

	for _, directory := range directories {
		log.Debugf("creating test directory: %s", directory)
		err = os.MkdirAll(directory, os.ModePerm)
		if err != nil {
			return
		}
	}

	files := []string{
		filepath.Join(paths.DotfilesDirectory, ".bash_profile"),
		filepath.Join(paths.DotfilesDirectory, ".gitconfig"),
		filepath.Join(paths.DotfilesDirectory, ".vimrc"),
	}

	for _, file := range files {
		log.Debugf("creating test file: %s", file)
		_, err = os.Create(file)
		if err != nil {
			return
		}
	}

	return
}
