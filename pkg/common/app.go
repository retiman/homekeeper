package common

import (
	"os"
	"path/filepath"
)

func Keep(ctx *Context) (err error) {
	if ctx.IsDebug {
		log = NewLogger("common", os.Stderr)
		log.Debug("ok...")
	}

	log.Debug("Starting 'keep' operation.")

	file := filepath.Join(ctx.HomeDirectory, ".homekeeper.yml")
	ctx.Config, err = readConfig(ctx, file)
	if err != nil {
		return
	}

	ctx.Excludes = make(map[string]bool)
	for _, exclude := range ctx.Config.Ignores {
		ctx.Excludes[exclude] = true
	}

	plan := make(map[string]string)
	for _, dotfilesDirectory := range ctx.Config.Directories {
		planSymlinks(ctx, dotfilesDirectory, plan)
	}
	if len(plan) == 0 {
		Writeln(ctx, "Nothing to symlink.")
		return
	}

	err = createSymlinks(ctx, plan)
	if err != nil {
		return
	}

	if !ctx.IsNoCleanup {
		_, err = removeBrokenSymlinks(ctx, ctx.HomeDirectory)
		if err != nil {
			return
		}
	}

	log.Debug("Ending 'keep' operation.")
	return
}

func Unkeep(ctx *Context) (err error) {
	if ctx.IsDebug {
		log = NewLogger("common", os.Stderr)
	}

	log.Debug("Starting 'unkeep' operation.")

	ctx.Excludes = make(map[string]bool)
	for _, exclude := range ctx.Config.Ignores {
		ctx.Excludes[exclude] = true
	}

	err = restoreSymlinks(ctx)

	log.Debug("Ending 'unkeep' operation.")
	return
}

func Cleanup(ctx *Context) (err error) {
	if ctx.IsDebug {
		log = NewLogger("common", os.Stderr)
	}

	log.Debug("Starting 'cleanup' operation.")

	_, err = removeBrokenSymlinks(ctx, ctx.HomeDirectory)

	log.Debug("Ending 'cleanup' operation.")
	return
}
