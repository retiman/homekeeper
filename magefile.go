// +build mage

package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/magefile/mage/sh"
)

func Clean() (err error) {
	sh.Rm("homekeeper")
	sh.Rm("homekeeper.exe")
	sh.Rm("tmp")
	return
}

func Format() (err error) {
	err = sh.Run("gofmt", "-w", "-s", "cmd")
	if err != nil {
		return
	}

	err = sh.Run("gofmt", "-w", "-s", "pkg")
	if err != nil {
		return
	}

	err = sh.Run("gofmt", "-w", "-s", "magefile.go")
	if err != nil {
		return
	}

	return
}

func Build() (err error) {
	flags, err := GetFlags()
	if err != nil {
		return
	}

	err = sh.Run("go", "build", fmt.Sprintf("-ldflags='%s'", flags), ".")
	if err != nil {
		return
	}

	return
}

func Test() (err error) {
	err = sh.RunV("go", "test", "./cmd/...")
	if err != nil {
		return
	}

	err = sh.RunV("go", "test", "./pkg/...")
	if err != nil {
		return
	}

	return
}

func GetFlags() (flags string, err error) {
	build, err := sh.Output("git", "rev-parse", "--short", "HEAD")
	if err != nil {
		return
	}

	bytes, err := os.ReadFile("VERSION")
	if err != nil {
		return
	}

	module := "github.com/retiman/homekeeper"
	version := strings.TrimSpace(string(bytes))
	flags = strings.Join(
		[]string{
			fmt.Sprintf("-X %s/cmd.Build=%s", module, build),
			fmt.Sprintf("-X %s/cmd.Version=%s", module, version),
		},
		" ",
	)

	return
}
