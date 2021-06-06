package cmd

import (
	"github.com/retiman/homekeeper/pkg/common"
)

func init() {
	log = common.NewDebugLogger()
}
