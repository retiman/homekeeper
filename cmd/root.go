package cmd

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"

	"github.com/retiman/homekeeper/pkg/common"
	"github.com/spf13/cobra"
)

var (
	context = &common.Context{}
)

var (
	rootCommand    *cobra.Command
	initCommand    *cobra.Command
	cleanupCommand *cobra.Command
	keepCommand    *cobra.Command
	unkeepCommand  *cobra.Command
	versionCommand *cobra.Command
)

// In golang, the init() function is special; it's automatically executed on a per-file basis, and each file can contain
// an init() function.  Because we might want to re-setup the command line interface during a test, we have to make
// this a separate function.
func setup() {
	initCommand = &cobra.Command{
		Use:   "init",
		Short: "Sets your dotfiles directory, possibly from a git clone.",
		Args: func(_ *cobra.Command, args []string) (err error) {
			if len(args) > 1 {
				return errors.New("expecting 0 or 1 arguments")
			}

			return
		},
		RunE: func(_ *cobra.Command, _ []string) error {
			return common.Init(context)
		},
	}
	initCommand.Flags().BoolVar(
		&context.IsGit,
		"git",
		false,
		"Assumes repository argument and will attempt to git clone first.",
	)
	initCommand.Flags().BoolVar(
		&context.IsNoKeep,
		"no-keep",
		false,
		"Does not run 'keep' after init.",
	)

	cleanupCommand = &cobra.Command{
		Use:   "cleanup",
		Short: "Removes broken symlinks in your home directory.",
		RunE: func(_ *cobra.Command, _ []string) error {
			return common.Cleanup(context)
		},
	}

	keepCommand = &cobra.Command{
		Use:   "keep",
		Short: "Symlinks dotfiles to your home directory from another location.",
		RunE: func(_ *cobra.Command, _ []string) error {
			return common.Keep(context)
		},
	}
	keepCommand.Flags().BoolVar(
		&context.IsNoCleanup,
		"no-cleanup",
		false,
		"Do not remove broken symlinks afterwards.",
	)
	keepCommand.Flags().BoolVar(
		&context.IsNoOverwrite,
		"no-overwrite",
		false,
		"Do not overwrite existing files/directories.",
	)

	unkeepCommand = &cobra.Command{
		Use:   "unkeep",
		Short: "Replaces symlinks in your home directory with symlinked files.",
		RunE: func(_ *cobra.Command, _ []string) error {
			return common.Unkeep(context)
		},
	}

	versionCommand = &cobra.Command{
		Use:   "version",
		Short: "Prints the version and then exists.",
		RunE: func(_ *cobra.Command, _ []string) (_ error) {
			fmt.Printf("Version %s\n", Build)
			fmt.Printf("Build %s\n", Build)
			return
		},
	}

	rootCommand = &cobra.Command{
		Use:              "homekeeper",
		Short:            "Homekeeper symlinks dotfiles to your home directory.",
		PersistentPreRun: prePersistentRun,
	}
	rootCommand.PersistentFlags().BoolVar(
		&context.IsDryRun,
		"dry-run",
		false,
		"Enables dry run mode (no changes will be made).",
	)
	rootCommand.PersistentFlags().BoolVar(
		&context.IsDebug,
		"debug",
		false,
		"Enables debug output in addition to normal output.",
	)
	rootCommand.PersistentFlags().BoolVar(
		&context.IsQuiet,
		"quiet",
		false,
		"Enables quiet mode (will not output anything)",
	)

	rootCommand.AddCommand(initCommand)
	rootCommand.AddCommand(cleanupCommand)
	rootCommand.AddCommand(keepCommand)
	rootCommand.AddCommand(unkeepCommand)
	rootCommand.AddCommand(versionCommand)
}

func prePersistentRun(_ *cobra.Command, args []string) {
	if context.IsQuiet {
		// Quiet implies no debugging output either.
		context.IsDebug = false
	}

	if context.IsDebug {
		// There isn't a way to enable/disable logging with go-logger except to change where the output goes.
		log = common.NewLogger("cmd", os.Stderr)
	}

	homeDirectory, err := os.UserHomeDir()
	if err != nil {
		common.Writeln(context, "Couldn't determine home directory!")
		os.Exit(1)
	}

	context.HomeDirectory = homeDirectory
	context.ConfigFile = filepath.Join(context.HomeDirectory, ".homekeeper.yml")

	if len(args) == 1 {
		context.DotfilesLocation = args[0]
	}

	log.Debugf("Invoked with context: %+v", context)
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
