package cmd

import (
	"github.com/spf13/cobra"
)

var (
	cleanupCommand *cobra.Command
)

func createCleanupCommand() *cobra.Command {
	return &cobra.Command{
		Use:   "cleanup",
		Short: "Removes broken symlinks in your home directory.",
		Run: createRunHandler(func() {
			log.Infof("Command cleanup was called!")
		}),
	}
}
