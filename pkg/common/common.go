package common

import (
	"io"
)

type Context struct {
	Config        *Config
	ConfigFile    string
	IsDryRun      bool
	IsOverwrite   bool
	IsQuiet       bool
	HomeDirectory string
	Excludes      map[string]bool
}

// In golang, init() functions are run in lexical file name order.  Renaming files can cause the init functions to
// execute in a different order, which may produce unintended effects (for example, we'd like the log to be defined
// first).  Therefore, the convention in this project is to only have init() functions in the go files with the same
// name as the package.
func init() {
	log = NewLogger("common", io.Discard)
}

func Keep(ctx *Context) (err error) {
	ctx.Config, err = readConfig(ctx.HomeDirectory)
	if err != nil {
		panic(err)
	}

	ctx.Excludes = make(map[string]bool)
	for _, exclude := range ctx.Config.Ignores {
		ctx.Excludes[exclude] = true
	}

	plan := make(map[string]string)
	for _, dotfilesDirectory := range ctx.Config.Directories {
		planSymlinks(ctx, dotfilesDirectory, plan)
	}

	err = createSymlinks(ctx, plan)
	return
}

func Unkeep(ctx *Context) (err error) {
	return
}

func Cleanup(ctx *Context) (err error) {
	return
}
