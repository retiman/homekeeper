package cmd

import (
	"github.com/spf13/cobra"
)

func newCleanupCommand() *cobra.Command {
	return &cobra.Command{
		Use:   "cleanup",
		Short: "Removes broken symlinks in your home directory.",
	}
}

func cleanup(flags *Flags) {
}
