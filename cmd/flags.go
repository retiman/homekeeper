package cmd

type Flags struct {
	IsDebug  bool
	IsDryRun bool
}

var (
	flags = &Flags{}
)
