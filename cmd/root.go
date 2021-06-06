package cmd

import (
	"fmt"
	"os"

	"github.com/retiman/homekeeper/pkg/common"
	"github.com/spf13/cobra"
)

type Flags struct {
	IsDebug  bool
	IsDryRun bool
}

var (
	log         = common.NewDefaultLogger()
	flags       = &Flags{}
	rootCommand *cobra.Command
)

func init() {
	initCommands()
}

func initCommands() {
	rootCommand = createRootCommand()
	cleanupCommand = createCleanupCommand()
	keepCommand = createKeepCommand()
	unkeepCommand = createUnkeepCommand()
	versionCommand = createVersionCommand()

	rootCommand.AddCommand(cleanupCommand)
	rootCommand.AddCommand(keepCommand)
	rootCommand.AddCommand(unkeepCommand)
	rootCommand.AddCommand(versionCommand)
}

func createRootCommand() *cobra.Command {
	command := &cobra.Command{
		Use:   "homekeeper",
		Short: "Homekeeper symlinks dotfiles to your home directory.",
		Run: createRunHandler(func() {
			log.Infof("Command root was called!")
		}),
	}
	command.PersistentFlags().BoolVar(
		&flags.IsDryRun,
		"dry-run",
		false,
		"Enables dry run mode (no changes will be made).",
	)
	command.PersistentFlags().BoolVarP(
		&flags.IsDebug,
		"debug",
		"v",
		false,
		"Enables debug output.",
	)
	return command
}

// Creates a run handler for a command; this is the function that will be invoked when the user runs
// `homekeeper <command>`.
func createRunHandler(handler func()) func(*cobra.Command, []string) {
	return func(cmd *cobra.Command, args []string) {
		if flags.IsDebug {
			log = common.NewDebugLogger()
			common.SetDebugLogger()
		}

		log.Debugf("invoked with flags: %+v", flags)
		handler()
	}
}

func Execute() {
	err := rootCommand.Execute()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
