package common

import (
	"os"

	"gopkg.in/yaml.v3"
)

type Config struct {
	Directories []string `yaml:"directories"`
	Ignores     []string `yaml:"ignores"`
}

func readConfig(ctx *Context, file string) (config *Config, err error) {
	log.Debugf("Reading config file: %s", file)

	content, err := os.ReadFile(file)
	if err != nil {
		Writeln(ctx, "Couldn't read config file: %s", file)
		log.Errorf("Couldn't read config file: %+v", err)
		return
	}

	config = &Config{}
	err = yaml.Unmarshal(content, config)
	if err != nil {
		Writeln(ctx, "Couldn't parse config file: %s", file)
		log.Errorf("Couldn't parse config file: %+v", err)
		return
	}

	Writeln(ctx, "Read config file: %s", file)
	log.Debugf("Read config: %+v", config)
	return
}

func writeConfig(ctx *Context, file string, config *Config) (err error) {
	log.Debugf("Writing config: %+v", config)
	bytes, err := yaml.Marshal(config)
	if err != nil {
		Writeln(ctx, "Couldn't write config file: %s", file)
		log.Errorf("Couldn't marshal configuration: %+v", config)
		return
	}

	err = os.WriteFile(file, bytes, 0644)
	if err != nil {
		Writeln(ctx, "Couldn't write config file: %s", file)
		log.Errorf("Couldn't write config file: %+v", err)
		return
	}

	Writeln(ctx, "Wrote config file: %s", file)
	return
}
