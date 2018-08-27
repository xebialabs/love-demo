# DevOps as Code workshop

This workshop will teach you:

* How to start up the XL DevOps Platform with the devops-as-code features installed.
* How to install the XL CLI.
* How to import and deploy a Docker application with XL Deploy.
* How to import and run a pipeline with XL Release.

## Prerequisites

you'll need to have the following software installed on your machine before you begin:
* Git
* Docker
  * Mac: https://docs.docker.com/docker-for-mac/
  * Windows: https://docs.docker.com/docker-for-windows/
  * Linux: Refer to the instructions for your Linux distribution on how to install Docker

# Get the workshop

1) Clone this repository with Git:
```
$ git clone git@github.com:xebialabs/devops-as-code-demo.git
$ cd devops-as-code-demo
$ git checkout -q devops-as-code-workshop-1
```

# Start up the XL DevOps Platform

1) If you are already running XL Deploy or XL Release on your local machine, please stop them.

2) Start up the XL DevOps Platform:
```
$ docker-compose up --build
```

3) Wait for XL Deploy and XL Release to have started up. This will have occurred when the following line is shown in the logs:
```
devops-as-code-demo_xl-cli_1 exited with code 0
```

# Install the XL CLI

1) Install the XL command line client:

## Mac
```
$ curl -o xl https://s3.amazonaws.com/xl-cli/bin/8.2.0-workshop.1/darwin-amd64/xl
$ chmod +x xl
$ sudo mv xl /usr/local/bin
```

## Linux
```
$ curl -o xl https://s3.amazonaws.com/xl-cli/bin/8.2.0-workshop.1/linux-amd64/xl
$ chmod +x xl
$ sudo mv xl /usr/local/bin
```

## Windows
```
> curl -o xl.exe https://s3.amazonaws.com/xl-cli/bin/8.2.0-workshop.1/windows-amd64/xl.exe
```

# Exercise 1: Review the XL DevOps platform runNing on Docker

When the XL DevOps Platform was started up by [the Docker Compose file](https://github.com/xebialabs/devops-as-code-demo/blob/devops-as-code-workshop-1/docker-compose.yaml), four containers were started:
* `xl-deploy` runs XL Deploy. You can access it at http://localhost:4516/ and login with the username `admin` and password `admin`.
* `xl-release` runs XL Release. You can access it at http://localhost:5516/ and login with the username `admin` and password `admin`.
* `dockerproxy` runs a proxy to allow the XL Deploy instance running in the `xl-deploy` container to connect to the Docker engine in which it is running.
* `xl-cli` runs the XL CLI to apply the [`configure-xl-devops-platform.yaml`](https://github.com/xebialabs/devops-as-code-demo/blob/devops-as-code-workshop-1/config/configure-xl-devops-platform.yaml) YAML file. This XL YAML file adds two configurations:
  * It adds an XL Deploy configuration to XL Release so that the latter can find the former.
  * It adds a `docker.Engine` configuration to XL Deploy so that XL Deploy can deploy to the Docker engine (via the Docker proxy).

1) Open the XL Deploy GUI, find the **local-docker** entry in the Infrastructure tree and run the **Check Connection** control task.


# Exercise 2: Set up the environment

Now that we have the XL DevOps Platform up and runnning and connected to our local Docker instance, let's create an environment that contains it.

1) Open a new terminal window and go to the directory where you checked out the `devops-as-code-workshop` repository.

2) Create the environment that contains the Docker engine by applying its XL YAML file:
```
$ xl apply -f workshop/exercise-2/docker-environment.yaml
```
3) Open the XL Deploy GUI and review the environment that you just created.

# Exercise 3: Import a simple application and deploy it

Let's try and deploy something to our local Docker instance with XL Deploy. We'll start with a single container; the backend part of the REST-o-rant application. It's called **rest-o-rant-api** because it serves up the API.

1) Import the REST-o-rant-api package:

```
$ xl apply -f workshop/exercise-3/rest-o-rant-api-docker.yaml
```

2) Open the XL Deploy GUI and review version **1.0** of the **rest-o-rant-api-docker** application. Compare it with the contents of the YAML file that you applied in the previous step.

3) Deploy version **1.0** of the **rest-o-rant-api-docker** application to the **Local Docker Engine** environment.

4) When the deployment has finished, open a new terminal window and type
```
$ docker ps
```
The container **rest-o-rant-api** should be running.

# Exercise 4: Deploy a (slight) more complex application

Serving a REST API is all nice and dandy, but it's pretty useless without a UI. So let's deploy the **rest-o-rant-web** container. Because it needs to access the **rest-o-rant-api** application to get its data, we'll also need to define a Docker network to allow the two containers to communicate. Version **1.1** of the **rest-o-rant-api** application will define that network.

1) Import the new REST-o-rant-api package, as well as the REST-o-rant-web package:
```
$ xl apply -f exercise-4/rest-o-rant-docker.yaml
```

2) Open the XL Deploy GUI and review the two packages that you just imported and compare them with the YAML file. Notice the net **rest-o-rant-network** deployable in the **rest-o-rant-api** package, as well as the application dependencies and the orchestrator set on the **rest-o-rant-web** package.

3) Deploy version **1.0** of the **rest-o-rant-web** package to the **Local Docker Engine** environment.

4) When the deployment has finished, open a new browser tab and access it at http://localhost/. You should see a text saying "Find the best restaurants near you!".
Type "Cow" in the search bar and click "Search" to find the "Old Red Cow" restaurant.

# Exercise 5: Import a simple pipeline

OK, we've deployed the application, but how do we get rid of it? Well, let's do that manually for one last time:

1) Undeploy the **rest-o-rant-web** application from the **Local Docker Engine** environment.

But let's make sure that you don't forget next time that you run this workshop. Let's create a simple pipeline.

2) Import that REST-o-rant pipeline:
```
$ xl apply -f rest-o-rant-docker-pipeline.yaml
```

3) Open the XL Release GUI and review the **REST-o-rant on Docker** pipeline that you've just imported.

4) Start a new release from that template and follow the instructions.

# Bonus exercise: putting it all together

OK, that was cool and all. But I had to run the `xl apply` command line four times to get everything into XL Deploy and XL Release. That's nice for a workshop, but not so nice for a demo.

1) Bring down your XL DevOps Platform to start with a clean slate:
```
$ docker-compose down
```

2) Create a YAML file that combines all the exercises we've done so that you can get the demo up and running with two simple commands:
```
$ docker-compose up
$ xl apply -f rest-o-rant-demo.yaml
```
