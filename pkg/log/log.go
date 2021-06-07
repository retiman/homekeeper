package log

import (
	"fmt"
	"log"
)

const (
	DEBUG = iota
	INFO
)

var (
	Level = INFO
)

func init() {
	log.SetFlags(log.Lshortfile)
}

func Debugf(format string, a ...interface{}) {
	if Level != DEBUG {
		return
	}

	log.Printf("[DEBUG] "+format, a...)
}

func Infof(format string, a ...interface{}) {
	if Level != DEBUG {
		fmt.Printf(format, a...)
		return
	}

	log.Printf("[INFO] "+format, a...)
}

func Warnf(format string, a ...interface{}) {
	if Level != DEBUG {
		fmt.Printf(format, a...)
		return
	}

	log.Printf("[WARN] "+format, a...)
}

func Errorf(format string, a ...interface{}) {
	if Level != DEBUG {
		fmt.Printf(format, a...)
		return
	}

	log.Printf("[ERROR] "+format, a...)
}
