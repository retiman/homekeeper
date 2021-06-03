package common

import (
	"os"
	path "path/filepath"

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

func SetupFiles() (paths *Paths, err error) {
	cwd, err := os.Getwd()
	if err != nil {
		return
	}

	paths = &Paths{}
	paths.RootDirectory = path.Join(cwd, "testdata")
	paths.HomeDirectory = path.Join(paths.RootDirectory, "home", "johndoe")
	paths.DotfilesDirectory = path.Join(paths.HomeDirectory, "dotfiles")

	log.Debugf("removing all files in directory: %s", paths.RootDirectory)
	err = os.RemoveAll(paths.RootDirectory)
	if err != nil {
		return
	}

	directories := []string{
		paths.DotfilesDirectory,
		path.Join(paths.DotfilesDirectory, ".git"),
		path.Join(paths.DotfilesDirectory, ".vim"),
	}

	for _, directory := range directories {
		log.Debugf("creating test directory: %s", directory)
		err = os.MkdirAll(directory, os.ModePerm)
		if err != nil {
			return
		}
	}

	files := []string{
		path.Join(paths.DotfilesDirectory, ".bash_profile"),
		path.Join(paths.DotfilesDirectory, ".gitconfig"),
		path.Join(paths.DotfilesDirectory, ".vimrc"),
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
