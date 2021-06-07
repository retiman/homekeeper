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

func writeConfig(file string, config *Config) (err error) {
	log.Debugf("writing config file %+v: %s", config, file)
	bytes, err := yaml.Marshal(config)
	if err != nil {
		log.Errorf("error writing config: %+v", config)
		return
	}

	err = ioutil.WriteFile(file, bytes, 0644)
	if err != nil {
		log.Errorf("error writing config file: %s", file)
		return
	}

	return
}
