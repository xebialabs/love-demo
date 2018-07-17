# Python 3
import sys
import json
import yaml
import os

def main():
    fileArgument = sys.argv[1]

    data = read_yaml_file(fileArgument)

    # Print YAML
    print_as_yaml(data)

#
# Util
#

def print_as_yaml(list):
    for item in list:
        print(yaml.safe_dump(item, default_flow_style=False, explicit_start=True))

# Hack to properly print Yaml
# https://stackoverflow.com/questions/45004464/yaml-dump-adding-unwanted-newlines-in-multiline-strings
yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str
def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)
yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)

def read_yaml_file(fileArgument, data = []):
    with open(fileArgument, 'r') as stream:
        for fileData in yaml.load_all(stream):
            data.append(fileData)
    return data

def add_from_yaml_file(fileArgument, data):
    if not os.path.isfile(fileArgument):
        return

    with open(fileArgument, 'r') as stream:
        for fileData in yaml.load_all(stream):
            data.update(fileData)

    return data

#
# Yaml tag handler setup
#   !secret -- resolves value against a secrets file.
#   !value  -- resolves value against a values file.
#

secrets = {}
secretsFile = os.path.join(os.path.expanduser('~'), '.xl-config/secrets.yaml')
add_from_yaml_file(secretsFile, secrets)

def yaml_insert_secret(loader, node):
    key = loader.construct_scalar(node)
    if key in secrets:
        return secrets[loader.construct_scalar(node)]
    else:
        return key

yaml.add_constructor('!secret', yaml_insert_secret)


replacementValues = {}
defaultValuesFile = os.path.join(os.path.expanduser('~'), '.xl-config/default-values.yaml')
add_from_yaml_file(defaultValuesFile, replacementValues)
add_from_yaml_file('values.yaml', replacementValues)

def yaml_insert_value(loader, node):
    key = loader.construct_scalar(node)
    if key in replacementValues:
        return replacementValues[loader.construct_scalar(node)]
    else:
        return key

yaml.add_constructor('!value', yaml_insert_value)


# Execute script
main()
