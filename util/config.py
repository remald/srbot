import json


def load_configuration(file):
    with open(file, 'rb') as config:
        config_content = config.read()

    return json.loads(config_content)


__CONFIG__ = load_configuration('config.json')
