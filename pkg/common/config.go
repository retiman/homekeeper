package common

import (
	"gopkg.in/yaml.v2"
	"io/ioutil"

	"github.com/retiman/homekeeper/pkg/log"
)

type Config struct {
	Directories []string `yaml:"directories"`
	Ignores     []string `yaml:"ignores"`
}

func readConfig(file string) (config *Config, err error) {
	log.Debugf("reading config file: %s", file)
	content, err := ioutil.ReadFile(file)
	if err != nil {
		return
	}

	config = &Config{}
	err = yaml.Unmarshal(content, config)
	if err != nil {
		return
	}

	log.Debugf("read configuration: %+v", config)
	return
}
