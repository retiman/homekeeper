import json
import logging
import os
import homekeeper.exceptions
import homekeeper.lib


fopen = homekeeper.lib.fopen
lib = homekeeper.lib
ConfigException = homekeeper.exceptions.ConfigException
JSONDecodeError = json.JSONDecodeError


class ConfigData:
    def __init__(self):
        self.directories = []
        self.excludes = [
            '.git',
            '.gitignore',
            'LICENSE',
            'LICENSE.txt',
            'README',
            'README.md',
            'README.txt'
        ]


def get_default_location():
    return os.path.join(lib.get_home_directory(), '.homekeeper.json')


def read(config_file):
    try:
        if not config_file or not os.path.exists(config_file):
            config_file = os.path.abspath(os.path.join(os.getcwd(), '.homekeeper.json'))
            logging.info("trying configuration from current directory: %s", config_file)
        if not os.path.exists(config_file):
            config_file = get_default_location()
            logging.info("trying configuration from home directory :%s", config_file)
        if not os.path.exists(config_file):
            raise ConfigException("could not find configuration file anywhere; create .homekeeper.json first")
        return __read(config_file)
    except IOError as e:
        raise ConfigException("couldn't read from file '{}': {}".format(config_file, e))
    except JSONDecodeError as e:
        raise ConfigException("configuration format in file '{}' was invalid: {}".format(config_file, e))


def write(config_data, config_file=None):
    try:
        if not config_file:
            logging.info("writing configuration to default location: %s", get_default_location())
            config_file = get_default_location()
        return __write(config_data, config_file=config_file)
    except IOError as e:
        raise ConfigException("couldn't write to file '{}': {}".format(config_file, e))


def __read(config_file):
    with fopen(config_file, encoding='utf-8') as f:
        logging.debug("reading configuration from: %s", os.path.abspath(config_file))
        data = json.loads(f.read())
        logging.debug("read configuration: %s", data)
        config_data = ConfigData()
        __read_directories(config_data, data)
        __read_excludes(config_data, data)
        if not config_data.directories:
            raise ConfigException("no configuration key named 'directory' or 'directories' "
                                  "found: {}".format(config_file))
        if not config_data.excludes:
            config_data.excludes = []
        return config_data


def __write(config_data, config_file=None):
    with fopen(config_file, 'w', encoding='utf-8') as f:
        data = dict()
        data['directories'] = config_data.directories
        data['excludes'] = config_data.excludes
        json_data = json.dumps(data, sort_keys=True, indent=4)
        logging.debug("writing configuration: %s", json_data)
        f.write(json_data)
        logging.debug("wrote configuration to: %s", config_file)
        return config_file


def __read_directories(config_data, data):
    if 'directory' in data and 'directories' in data:
        raise ConfigException("configuration key 'directory' cannot be present with key 'directories'")
    if 'directories' in data and isinstance(data['directories'], list):
        config_data.directories = data['directories']
        for directory in config_data.directories:
            if not isinstance(directory, str):
                raise ConfigException("configuration key 'directories' did not contain a string: {}"
                                      .format(directory))
        return
    if 'directories' in data and isinstance(data['directories'], str):
        config_data.directories = [data['directories']]
        return
    if 'directory' in data and isinstance(data['directory'], str):
        config_data.directories = [data['directory']]
        return
    raise ConfigException("configuration key 'directories' and/or 'directory' is not a list or string")


def __read_excludes(config_data, data):
    if 'excludes' not in data:
        config_data.excludes = []
        return
    if not isinstance(data['excludes'], list):
        raise ConfigException("configuration key 'excludes' is not a list: {}".format(data['excludes']))
    config_data.excludes = data['excludes']
    for exclude in config_data.excludes:
        if not isinstance(exclude, str):
            raise ConfigException("configuration key 'excludes' did not contain a string: {}".format(exclude))
