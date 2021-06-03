package cmd

import (
	"github.com/spf13/cobra"
)

func newUnkeepCommand() *cobra.Command {
	return &cobra.Command{
		Use:   "unkeep",
		Short: "Replaces symlinks in your home directory with symlinked files.",
	}
}

func unkeep(flags *Flags) {
}
