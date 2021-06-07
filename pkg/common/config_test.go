package common

import (
	"io/ioutil"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestReadConfig(t *testing.T) {
	expected := &Config{
		Directories: []string{
			"/home/johndoe/dotfiles",
			"/home/johndoe/dotfiles2",
		},
		Ignores: []string{
			".git",
			"README.md",
		},
	}

	actual, err := readConfig(filepath.Join("testdata", "homekeeper.yml"))
	if err != nil {
		assert.Fail(t, err.Error())
	}

	assert.EqualValues(t, actual, expected)
}

func TestWriteConfig(t *testing.T) {
	config := &Config{
		Directories: []string{
			"/home/johndoe/dotfiles",
			"/home/johndoe/dotfiles2",
		},
		Ignores: []string{
			".git",
			"README.md",
		},
	}
	rootDirectory, err := getRepositoryRoot()
	if err != nil {
		assert.Fail(t, err.Error())
	}
	output := filepath.Join(rootDirectory, "tmp", "homekeeper.yml")

	writeConfig(output, config)

	expected, err := ioutil.ReadFile(filepath.Join("testdata", "homekeeper.yml"))
	if err != nil {
		assert.Fail(t, err.Error())
	}
	actual, err := ioutil.ReadFile(filepath.Join(output))
	if err != nil {
		assert.Fail(t, err.Error())
	}

	assert.Equal(t, string(actual), string(expected))
}
