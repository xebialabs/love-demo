# DevOps as Code workshop

This workshop will:

1. Teach you how to start up a copy of XL Deploy and XL Release with the devops-as-code features installed.
2. Teach you how to install the XL CLI.
3. Teach you how to import and run a deployment of a simple application to Docker.
4. Make you do modify the XL YAML files for that simple application and apply them again.
5. Give you a certificate! :-)

## Prerequisites

you'll need to have the following software installed on your machine before you begin:
* Git
* Docker
  * Mac: https://docs.docker.com/docker-for-mac/
  * Windows: https://docs.docker.com/docker-for-windows/
  * Linux: Refer to the instructions for your Linux distribution on how to install Docker


# Get the workshop

1. Clone this repository with Git:
```
$ git clone git@github.com:xebialabs/devops-as-code-demo.git
$ cd devops-as-code-demo
$ git checkout devops-as-code-workshop-1
```

# Start up the XL DevOps Platform

1. Start up the XL DevOps Platform:
```
$ docker-compose up --build
```

1. Wait for XL Deploy and XL Release to have started up. This will have occured when the following line is shown in the logs:
```
devops-as-code-demo_xl-cli_1 exited with code 0
```

# Install the XL CLI

Install the XL command line client:

## Mac
```
$ curl https://s3.amazonaws.com/xl-cli/bin/8.2.0-workshop.1/darwin-amd64/xl
$ chmod +x xl
$ sudo mv xl /usr/local/bin
```

## Linux
```
$ curl https://s3.amazonaws.com/xl-cli/bin/8.2.0-workshop.1/linux-amd64/xl
$ chmod +x xl
$ sudo mv xl /usr/local/bin
```

## Windows
```
> curl https://s3.amazonaws.com/xl-cli/bin/8.2.0-workshop.1/windows-amd64/xl.exe
```

# Deploy the demo application

1. Apply the XL YAML file:
```
$ xl apply -f workshop/rest-o-rant-docker.yaml
```
1. Open the XL Deploy UI at http://localhost:4516
1. Log in with username `admin` and password `admin`
1. In the Explorer tree, expand `Applications`, then `REST-o-rant`, then `rest-o-rant-web-docker`
1. Click on the three little dots on the right of `1.0` and select **Deploy**.
1. Select the *Docker Engine on Host* environment.
1. Click *Continue* in the top right corner.
1. Click *Deploy* in the top right corner.
1. Wait for the deployment to finish.
1. Open a new browser tab and access the application at http://localhost/
You should see a text saying "Find the best restaurants near you!".
Type "Cow" in the search bar and click "Search" to find the "Old Red Cow" restaurant.
