package cmd

import (
	"fmt"
	"os"

	"github.com/retiman/homekeeper/pkg/common"
	"github.com/spf13/cobra"
)

type CommandHandler func(*cobra.Command, []string) error
type Handler func(*common.Context) error

var (
	flags = &common.Context{}
)

var (
	rootCommand    *cobra.Command
	cleanupCommand *cobra.Command
	keepCommand    *cobra.Command
	unkeepCommand  *cobra.Command
	versionCommand *cobra.Command
)

// In golang, the init() function is special; it's automatically executed on a per-file basis, and each file can contain
// an init() function.  Because we might want to re-initialize the command line interface during a test, we have to make
// this a separate function.
func initialize() {
	cleanupCommand = &cobra.Command{
		Use:   "cleanup",
		Short: "Removes broken symlinks in your home directory.",
		RunE: func(_ *cobra.Command, _ []string) error {
			return common.Cleanup(flags)
		},
	}

	keepCommand = &cobra.Command{
		Use:   "keep",
		Short: "Overwrites dotfiles in your home directory by symlinking them from somewhere else.",
		RunE: func(_ *cobra.Command, _ []string) error {
			return common.Keep(flags)
		},
	}

	unkeepCommand = &cobra.Command{
		Use:   "unkeep",
		Short: "Replaces symlinks in your home directory with symlinked files.",
		RunE: func(_ *cobra.Command, _ []string) error {
			return common.Unkeep(flags)
		},
	}

	versionCommand = &cobra.Command{
		Use:   "version",
		Short: "Prints the version and then exists.",
		RunE: func(_ *cobra.Command, _ []string) error {
			fmt.Println(buildVersion)
			return nil
		},
	}

	rootCommand = &cobra.Command{
		Use:              "homekeeper",
		Short:            "Homekeeper symlinks dotfiles to your home directory.",
		PersistentPreRun: prePersistentRun,
	}
	rootCommand.PersistentFlags().BoolVar(
		&flags.IsDryRun,
		"dry-run",
		false,
		"Enables dry run mode (no changes will be made).",
	)
	rootCommand.PersistentFlags().BoolVar(
		&flags.IsDebug,
		"debug",
		false,
		"Enables debug output in addition to normal output.",
	)
	rootCommand.PersistentFlags().BoolVar(
		&flags.IsQuiet,
		"quiet",
		false,
		"Enables quiet mode (will not output anything)",
	)

	rootCommand.AddCommand(cleanupCommand)
	rootCommand.AddCommand(keepCommand)
	rootCommand.AddCommand(unkeepCommand)
	rootCommand.AddCommand(versionCommand)
}

func prePersistentRun(_ *cobra.Command, _ []string) {
	if flags.IsQuiet {
		// Quiet implies no debugging output either.
		flags.IsDebug = false
	}

	if flags.IsDebug {
		// There isn't a way to enable/disable logging with go-logger except to change where the output goes.
		log = common.NewLogger("cmd", os.Stderr)
	}

	log.Debugf("Invoked with flags: %+v", flags)
}

// Executes the root command.  Note that the sub command should not be executed; the first arg that Cobra Command passes
// to your application will be the sub command; based on this the appropriate sub command will be executed (note that)
// the root command's run handler will not be executed if a sub command is run.
func Execute() {
	err := rootCommand.Execute()
	if err != nil {
		os.Exit(1)
	}
}
