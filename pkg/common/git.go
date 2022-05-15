package common

import (
	"os"
	"path/filepath"
	"strings"

	git "github.com/go-git/go-git/v5"
)

func isGit(ctx *Context) bool {
	if ctx.IsGit {
		return true
	}

	if strings.HasSuffix(ctx.DotfilesLocation, ".git") && strings.Contains(ctx.DotfilesLocation, ":") {
		return true
	}

	return false
}

func getRepositoryName(url string) string {
	parts := strings.Split(url, "/")
	last := parts[len(parts)-1]
	return strings.TrimSuffix(last, ".git")
}

func gitClone(ctx *Context, directory string) (repoName string, err error) {
	repoName = getRepositoryName(ctx.DotfilesLocation)
	repoDirectory := filepath.Join(directory, repoName)

	log.Debugf("Attempting to git clone repository %s into: %s", ctx.DotfilesLocation, repoDirectory)
	_, err = git.PlainClone(repoDirectory, false /* isBare */, &git.CloneOptions{
		URL:      ctx.DotfilesLocation,
		Progress: os.Stderr,
	})
	if err != nil {
		return
	}

	return
}
