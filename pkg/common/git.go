package common

import (
	_ "os"
	"strings"

	_ "github.com/go-git/go-git/v5"
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

func clone(ctx *Context) (repoName string, err error) {
	//log.Debugf("Attempting to git clone repository: %s", ctx.DotfilesLocation)
	//_, err = git.PlainClone(cwd, false /* isBare */, &git.CloneOptions{
	//	URL: ctx.DotfilesLocation,
	//	Progress: os.Stderr,
	//})
	//if err != nil {
	//	return
	//}

	//return getRepositoryName(ctx.DotfilesLocation)
	return
}
