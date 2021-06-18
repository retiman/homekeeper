package common

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIsGit(t *testing.T) {
	ctx := setupFixtures()
	ctx.IsGit = false
	ctx.DotfilesLocation = "git@github.com:retiman/dotfiles.git"

	assert.True(t, isGit(ctx))

	ctx.IsGit = true
	ctx.DotfilesLocation = "./dotfiles"

	assert.True(t, isGit(ctx))

	ctx.IsGit = false
	ctx.DotfilesLocation = "./dotfiles"

	assert.False(t, isGit(ctx))
}

func TestGetRepositoryName(t *testing.T) {
	expected := "dotfiles"
	actual := getRepositoryName("git@github.com:retiman/dotfiles.git")

	assert.Equal(t, actual, expected)
}
