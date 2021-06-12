package common

import (
	"io/ioutil"

	"gopkg.in/yaml.v2"
)

type Config struct {
	Directories []string `yaml:"directories"`
	Ignores     []string `yaml:"ignores"`
}

func readConfig(file string) (config *Config, err error) {
	content, err := ioutil.ReadFile(file)
	if err != nil {
		log.Errorf("Couldn't read config file: %s", file)
		return
	}

	config = &Config{}
	err = yaml.Unmarshal(content, config)
	if err != nil {
		log.Errorf("Couldn't parse config file at %s: %v", file, err)
		return
	}

	log.Debugf("Read configuration: %+v", config)
	return
}

func writeConfig(file string, config *Config) (err error) {
	bytes, err := yaml.Marshal(config)
	if err != nil {
		log.Errorf("Couldn't marshal configuration: %+v", config)
		return
	}

	err = ioutil.WriteFile(file, bytes, 0644)
	if err != nil {
		log.Errorf("Couldn't write config file: %s", file)
		return
	}

	log.Debugf("Wrote config file: %s", file)
	return
}
