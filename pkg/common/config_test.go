package common

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestReadConfig(t *testing.T) {
	ctx := setupFixtures()

	actual, err := readConfig(ctx, filepath.Join("testdata", "homekeeper.yml"))
	if err != nil {
		assert.Fail(t, err.Error())
	}

	expected := &Config{
		Directories: []string{
			"/home/johndoe/d1",
			"/home/johndoe/d2",
			"/home/johndoe/d3",
		},
		Ignores: []string{
			"file1",
			"file2",
			"file3",
		},
	}
	assert.EqualValues(t, actual, expected)
}

func TestWriteConfig(t *testing.T) {
	ctx := setupFixtures()
	outputDirectory := filepath.Join(getRepositoryRoot(), "tmp")
	err := os.MkdirAll(outputDirectory, 0755)
	if err != nil {
		assert.Fail(t, err.Error())
	}

	outputFile := filepath.Join(getRepositoryRoot(), "tmp", "homekeeper.yml")
	config := &Config{
		Directories: []string{},
		Ignores:     []string{},
	}

	err = writeConfig(ctx, outputFile, config)
	if err != nil {
		assert.Fail(t, err.Error())
	}
	actual := readFileAsString(outputFile)

	expected := readFileAsString(filepath.Join("testdata", "empty.yml"))
	assert.Equal(t, string(actual), string(expected))
}
