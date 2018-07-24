# XL client demo scenarios

Demo scenarios showcasing the XL command line client for the XebiaLabs Devops Platform.

The demos show you how to import infrastructure, environments, deployment packages and provisioning packages into XL Deploy and to create a release pipeline in XL Release.

## Prerequisites
 * Docker
 * Git
 * Python 3.6 (for the Kubernetes demo scenarios)
 * Minikube (for the Kubernetes demo scenarios)

## Setup

### Server setup using Docker

Run the demo with our official docker images using the supplied docker-compose file.

Start XL Release and XL Deploy using the following command:

	docker-compose up -d

This will start the servers on default ports (XLD: 4516; XLR: 5516) with admin/admin access.

Store the `deployit-license.lic` and `xl-release-license.lic` license files in `~/.xl-config/` and they will be picked up by the containers.


### Command-line

Install the XL command-line client using the following command:

#### MacOS

Download the XL client command line with this command:

	curl -o xl https://s3.amazonaws.com/xl-cli/com/xebialabs/xl-cli/8.2.0-alpha.1/xl-cli-8.2.0-alpha.1-darwin_amd64_xl.bin

Make the binary executable:

	chmod +x xl

Move the binary on your path:

	sudo mv xl /usr/local/bin/


## General Usage

	xl apply -f <yaml-file>

Will send the contents of the YAML file the appropriate server, XL Release or XL Deploy.

For more information, see

    xl --help

### Run the Hello world example

Execute the following command:

	xl apply -f demo/HelloWorld.yaml

Open XL Deploy and locate an empty application called **HelloWorld** under **Applications**.


## Demos

The following demos are available. Click on the links to see the READMEs with further instructions.

* [Rest-o-rant Kubernetes](demo/rest-o-rant/) -- Set up a sample pipeline in Kubernetes.
* [AWS Provisioning](demo/aws-provisioning/) -- _not working yet_
