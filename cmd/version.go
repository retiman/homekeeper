package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var (
	buildVersion   = "0.0.0"
	versionCommand *cobra.Command
)

func createVersionCommand() *cobra.Command {
	return &cobra.Command{
		Use:   "version",
		Short: "Prints the version and then exists.",
		Run: createRunHandler(func() {
			fmt.Println(buildVersion)
		}),
	}
}
