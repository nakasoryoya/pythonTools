import configparser


def read_configuration(config_file, section):
    config = configparser.ConfigParser()
    config.read(config_file)
    return dict(config.items(section))
