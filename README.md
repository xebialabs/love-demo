# XL client demo scenarios

Demo scenarios showcasing the XL command line client for the XebiaLabs Devops Platform.

The demos show you how to import infrastructure, environments, deployment packages and provisioning packages into XL Deploy and to create a release pipeline in XL Release.

## Prerequisites

### Required software

* Docker
* Git
* Python 3.6 or up (for the Kubernetes and AWS ECS demo scenarios)
* Minikube (for the Kubernetes demo scenarios)


### Licenses

1. Create a directory called `.xl-config` in your home directory.
2. Put your XL Deploy licence file (`deployit-license.lic`) in that directory.
3. Put your XL Release licence file (`xl-release-license.lic`) in that directory.

### VPN

1. Connect to the XebiaLabs VPN using the Cisco AnyConnect Secure Moblity Client (to access the alpha images)

### Starting the XL Deploy and XL Release servers

Run the demo with our official docker images using the supplied docker-compose file.

Start XL Release and XL Deploy using the following command:

```
$ docker-compose up -d
```

This will start the servers and make them accessible as follows:

**XL Deploy:** http://localhost:4516/ (admin/admin)

**XL Release:** http://localhost:5516/ (admin/admin)


### Install the command-line (macOS)

Download the XL client command line with this command:

```
$	curl -o xl https://s3.amazonaws.com/xl-cli/com/xebialabs/xl-cli/8.2.0-alpha.1/xl-cli-8.2.0-alpha.1-darwin_amd64_xl.bin
```

Make the binary executable:

```
$	chmod +x xl
```

Move the binary on your path:

```
$	sudo mv xl /usr/local/bin/
```

## General Usage

```
$	xl apply -f <yaml-file>
```

Will send the contents of the YAML file the appropriate server, XL Release or XL Deploy.

For more information, see

```
$	xl --help
```

### Run the Hello world example

Execute the following command:

```
$	xl apply -f demo/HelloWorld.yaml
```

Open XL Deploy and locate an empty application called **HelloWorld** under **Applications**.


## Demos

The following demos are available. Click on the links to see the READMEs with further instructions.

* [Kubernetes](demo/k8s/) -- Set up a sample pipeline in Kubernetes.
