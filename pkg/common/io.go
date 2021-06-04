package common

import (
	"fmt"
	"os"
)

func ListEntries(directory string) (entries []os.FileInfo, err error) {
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
		err = fmt.Errorf("not a directory: %s", directory)
		return
	}

	// Read all entries.
	return fh.Readdir(-1)
}
