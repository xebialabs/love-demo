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

	curl -o xl https://s3-eu-west-1.amazonaws.com/xl-client/macos/xl

Make the binary executable:

	chmod +x xl

Move the binary on your path:

	sudo mv xl /usr/local/bin/


## General Usage

	xl apply -f <yaml-file>

Will send the contents of the YAML file the appropriate server, XL Release or XL Deploy.

For more information, see

    xl --help
    
    
## Demos 

### Rest-o-Rant Kubernetes

#### Step 1. Configuring Minikube in XL Deploy

Make sure you have a running minikube environment locally.

Use the `kubeconfig2xld.py`  in the `config` directory to create XL YAML files that will create the Kubernetes environment in XL Deploy.

	python config/kubeconfig2xld.py > KubeConfig.yaml
	
Now send this file to XL Deploy using

	xl apply -f KubeConfig.yaml
	
### Step 2. Importing the Rest-o-rant application

Use thew following command to import the Rest-o-rant application or Kubernetes into XL Deploy.

	xl apply -f demo/kubernetes-rest-o-rant/rest-o-rant-package.yaml
	
### Step 3. Run the pipeline in XL Release

Create a template in XL Release using

	xl apply -f demo/kubernetes-rest-o-rant/pipeline.yaml
	
Now go to the XL Release UI running on http://localhost:5516.
Go to **Design > Templates** and locate the **Rest-o-rant Kubernetes** template.

Create a new release from the template, start it and follow the release flow.
	
	




