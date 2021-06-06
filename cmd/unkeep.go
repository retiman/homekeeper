package cmd

import (
	"github.com/spf13/cobra"
)

var (
	unkeepCommand *cobra.Command
)

func createUnkeepCommand() *cobra.Command {
	return &cobra.Command{
		Use:   "unkeep",
		Short: "Replaces symlinks in your home directory with symlinked files.",
		Run: createRunHandler(func() {
			log.Infof("Command unkeep was called!")
		}),
	}
}
