package cmd

import (
	"github.com/spf13/cobra"
)

func newRootCommand(flags *Flags) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "homekeeper",
		Short: "Homekeeper symlinks dotfiles to your home directory.",
	}
	cmd.PersistentFlags().BoolVar(
		&flags.IsDryRun,
		"dry-run",
		false,
		"Enables dry run mode (no changes will be made).",
	)
	cmd.PersistentFlags().BoolVarP(
		&flags.IsDebug,
		"debug",
		"v",
		false,
		"Enables debug output.",
	)
	return cmd
}

func root(flags *Flags) {
}
