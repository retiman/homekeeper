package log

import (
	"log"
	"os"

	"github.com/hashicorp/logutils"
)

var (
	debug  = logutils.LogLevel("DEBUG")
	info   = logutils.LogLevel("INFO")
	filter = &logutils.LevelFilter{
		Levels:   []logutils.LogLevel{"DEBUG", "INFO", "WARN", "ERROR"},
		MinLevel: logutils.LogLevel("INFO"),
		Writer:   os.Stderr,
	}
)

func init() {
	log.SetOutput(filter)
	SetInfoLevel()
}

func Debugf(format string, a ...interface{}) {
	log.Printf("[DEBUG] "+format, a...)
}

func Infof(format string, a ...interface{}) {
	log.Printf("[INFO] "+format, a...)
}

func Warnf(format string, a ...interface{}) {
	log.Printf("[WARN] "+format, a...)
}

func Errorf(format string, a ...interface{}) {
	log.Printf("[ERROR] "+format, a...)
}

func SetDebugLevel() {
	filter.SetMinLevel(logutils.LogLevel("DEBUG"))
	log.SetOutput(filter)
	log.SetFlags(log.Lshortfile)
}

func SetInfoLevel() {
	filter.SetMinLevel(logutils.LogLevel("INFO"))
	log.SetOutput(filter)
	log.SetFlags(0)
}
