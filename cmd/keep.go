package cmd

import (
	"github.com/spf13/cobra"
)

func newKeepCommand(flags *Flags) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "keep",
		Short: "Overwrites dotfiles in your home directory by symlinking them from somewhere else.",
	}
	cmd.Flags().BoolVar(
		&flags.IsNoCleanup,
		"no-cleanup",
		false, /* default */
		"Do not remove broken symlinks afterwards.",
	)
	return cmd
}

func keep(flags *Flags) {
}
