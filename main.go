package main

import (
	"github.com/retiman/homekeeper/cmd"
)

func main() {
	app := cmd.New()
	app.Execute()
}
