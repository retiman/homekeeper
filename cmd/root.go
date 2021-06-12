package cmd

import (
	"fmt"
	"os"

	"github.com/retiman/homekeeper/pkg/common"
	"github.com/spf13/cobra"
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
		Run: createRunHandler(func() {
			log.Infof("Command cleanup was called!")
		}),
	}

	keepCommand = &cobra.Command{
		Use:   "keep",
		Short: "Overwrites dotfiles in your home directory by symlinking them from somewhere else.",
		Run: createRunHandler(func() {
			log.Infof("Command keep was called!")
		}),
	}

	unkeepCommand = &cobra.Command{
		Use:   "unkeep",
		Short: "Replaces symlinks in your home directory with symlinked files.",
		Run: createRunHandler(func() {
			log.Infof("Command unkeep was called!")
		}),
	}

	versionCommand = &cobra.Command{
		Use:   "version",
		Short: "Prints the version and then exists.",
		Run: createRunHandler(func() {
			fmt.Println(buildVersion)
		}),
	}

	rootCommand = &cobra.Command{
		Use:   "homekeeper",
		Short: "Homekeeper symlinks dotfiles to your home directory.",
		Run: createRunHandler(func() {
			log.Infof("Command root was called!")
		}),
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

// We'd like to set the logging level and format based on user input.  Because we'd like to do this after the args have
// been parsed but before a run handler has executed for any particular command, we have to wrap the call to any
// particular run handled and set the Debugfging level based on parsed flags.
func createRunHandler(handler func()) func(*cobra.Command, []string) {
	return func(cmd *cobra.Command, args []string) {
		if flags.IsQuiet {
			// Quiet implies no debugging output.
			flags.IsDebug = false

			// Unless an abstraction like a common.App struct is created, we'll have to toggle the flag in the common package
			// as well.
			common.IsQuiet = true
		}

		if flags.IsDebug {
			// There isn't a way to enable/disable logging with go-logger except to change where the output goes.
			log = common.NewLogger("cmd", os.Stderr)

			// Unless an abstraction like a common.App struct is created, we'll have to toggle the flag in the common package
			// as well.
			common.EnableLogging()
		}

		log.Debugf("Invoked with flags: %+v", flags)
		handler()
	}
}

// Executes the root command.  Note that the sub command should not be executed; the first arg that Cobra Command passes
// to your application will be the sub command; based on this the appropriate sub command will be executed (note that)
// the root command's run handler will not be executed if a sub command is run.
func Execute() {
	err := rootCommand.Execute()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
