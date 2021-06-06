package cmd

import (
	"github.com/spf13/cobra"
)

var (
	keepCommand *cobra.Command
)

func createKeepCommand() *cobra.Command {
	return &cobra.Command{
		Use:   "keep",
		Short: "Overwrites dotfiles in your home directory by symlinking them from somewhere else.",
		Run: createRunHandler(func() {
			log.Infof("Command keep was called!")
		}),
	}
}
