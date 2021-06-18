package common

import (
	"io"
)

type Context struct {
	Config           *Config
	ConfigFile       string
	IsDebug          bool
	IsDryRun         bool
	IsGit            bool
	IsNoCleanup      bool
	IsNoKeep         bool
	IsNoOverwrite    bool
	IsQuiet          bool
	HomeDirectory    string
	DotfilesLocation string
	Excludes         map[string]bool
}

// In golang, init() functions are run in lexical file name order.  Renaming files can cause the init functions to
// execute in a different order, which may produce unintended effects (for example, we'd like the log to be defined
// first).  Therefore, the convention in this project is to only have init() functions in the go files with the same
// name as the package.
func init() {
	log = NewLogger("common", io.Discard)
}
