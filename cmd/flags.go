package cmd

type Flags struct {
	IsDebug  bool
	IsQuiet  bool
	IsDryRun bool
}

var (
	flags = &Flags{}
)
