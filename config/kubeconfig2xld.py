#!/usr/bin/env python3
import sys
import json
import yaml
import os

def main():
    # Get Kubernetes config file name location from command line or revert to default location if not specified
    fileArgument = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser('~'), '.kube/config')

    # Convert to XLD structure
    infrastructure = k8_config_to_infrastructure(fileArgument)
    environment = k8_environment(infrastructure)

    # Print YAML
    print_as_yaml(environment)
    print("---")
    print_as_yaml(infrastructure)

#
# Util
#
def print_as_json(dict):
    print(json.dumps(dict, indent=2, sort_keys=True))

def print_as_yaml(dict):
    print(yaml.safe_dump(dict, default_flow_style=False))

# Hack to properly print Yaml
# https://stackoverflow.com/questions/45004464/yaml-dump-adding-unwanted-newlines-in-multiline-strings
yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str
def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)
yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def read_yaml_file(fileArgument, data = []):
    with open(fileArgument, 'r') as stream:
        for fileData in yaml.load_all(stream):
            data.append(fileData)
    return data


#
# Create XLD YAML from Kubernetes Config
#

def k8_config_to_infrastructure(file):

    # Read Kubernetes config file
    config = read_yaml_file(file)[0]

    # Build CI for XL Deploy
    infrastructure = {
        'apiVersion': 'xl-deploy/v1beta1',
        'kind': 'Infrastructure',
        'spec': []
    }


    name = config['current-context']
    context = get_k8_context(config, name)
    cluster = get_k8_cluster(config, context['cluster'])
    user = get_k8_user(config, context['user'])

    k8master = {
        'name': 'Infrastructure/' + name,
        'type': 'k8s.Master',
        'apiServerURL': cluster['server'],
        'caCert': read_file(cluster['certificate-authority']),
        'tlsCert': read_file(user['client-certificate']),
        'tlsPrivateKey': read_file(user['client-key'])
    }

    namespace = {
        'name': 'default',
        'type': 'k8s.Namespace',
    }

    k8master['children'] = [namespace]
    infrastructure['spec'].append(k8master)

    return infrastructure

def k8_environment(infrastructure):
    environment = {
        'apiVersion': 'xl-deploy/v1beta1',
        'kind': 'Environments',
        'spec': [
            {
                'name': 'Kubernetes',
                'type': 'udm.Environment',
                'members': [
                    infrastructure['spec'][0]['name'],
                    infrastructure['spec'][0]['name'] + '/default'
                ]
            }
        ]
    }

    return environment

def get_k8_context(config, name):
    for context in config['contexts']:
        if context['name'] == name:
            return context['context']
    return None

def get_k8_cluster(config, name):
    for cluster in config['clusters']:
        if cluster['name'] == name:
            return cluster['cluster']
    return None

def get_k8_user(config, name):
    for user in config['users']:
        if user['name'] == name:
            return user['user']
    return None

# Execute script
main()
