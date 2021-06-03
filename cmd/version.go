package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

var BuildVersion = "0.0.0"

func newVersionCommand() *cobra.Command {
	return &cobra.Command{
		Use:   "version",
		Short: "Prints the version and then exists.",
	}
}

func version(flags *Flags) {
	fmt.Println(BuildVersion)
}
