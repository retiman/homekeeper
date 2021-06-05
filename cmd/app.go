package cmd

import (
	"fmt"
	"os"

	log "github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

type Handler func(flags *Flags)

type Flags struct {
	ConfigPath    string
	DirectoryPath string
	GitRepoURL    string
	IsNoCleanup   bool
	IsDebug       bool
	IsDryRun      bool
}

type CliApp struct {
	flags          *Flags
	rootCommand    *cobra.Command
	cleanupCommand *cobra.Command
	keepCommand    *cobra.Command
	unkeepCommand  *cobra.Command
	versionCommand *cobra.Command
}

func New() *CliApp {
	app := new(CliApp)
	app.flags = new(Flags)

	cmd := newRootCommand(app.flags)
	cmd.Run = app.createHandler(root)
	app.rootCommand = cmd

	cmd = newCleanupCommand()
	cmd.Run = app.createHandler(cleanup)
	app.cleanupCommand = cmd
	app.rootCommand.AddCommand(cmd)

	cmd = newKeepCommand(app.flags)
	cmd.Run = app.createHandler(keep)
	app.keepCommand = cmd
	app.rootCommand.AddCommand(cmd)

	cmd = newUnkeepCommand()
	cmd.Run = app.createHandler(unkeep)
	app.unkeepCommand = cmd
	app.rootCommand.AddCommand(cmd)

	cmd = newVersionCommand()
	cmd.Run = app.createHandler(version)
	app.versionCommand = cmd
	app.rootCommand.AddCommand(cmd)

	return app
}

func (app *CliApp) Execute() {
	if err := app.rootCommand.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func (app *CliApp) createHandler(handler Handler) func(*cobra.Command, []string) {
	return func(cmd *cobra.Command, args []string) {
		log.SetFormatter(&log.TextFormatter{
			DisableTimestamp: true,
			PadLevelText:     true,
			QuoteEmptyFields: true,
		})

		if app.flags.IsDebug {
			log.SetLevel(log.DebugLevel)
		}

		log.Debugf("invoked with flags: %+v", app.flags)

		handler(app.flags)
	}
}
