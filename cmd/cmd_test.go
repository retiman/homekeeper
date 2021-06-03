package cmd

import (
	"github.com/spf13/cobra"
)

func NewTracingHandler(isCalled *bool) func(*cobra.Command, []string) {
	return func(_ *cobra.Command, _ []string) {
		*isCalled = true
	}
}
