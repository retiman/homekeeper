package common

import (
	"io"
)

var (
	IsDryRun bool
	IsQuiet  bool
)

// In golang, init() functions are run in lexical file name order.  Renaming files can cause the init functions to
// execute in a different order, which may produce unintended effects (for example, we'd like the log to be defined
// first).  Therefore, the convention in this project is to only have init() functions in the go files with the same
// name as the package.
func init() {
	IsDryRun = false
	IsQuiet = false

	log = NewLogger("common", io.Discard)
}
