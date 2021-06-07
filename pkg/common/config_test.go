package common

import (
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
