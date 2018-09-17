# JenkinsWorld demo

This is the setup for the JenkinsWorld 2018 demo in San Francisco.

## Demo Set up

### Set up Docker & CLI

First, set up Docker and the XL client using the first step of the [DevOps as Code workshop](https://github.com/xebialabs/devops-as-code-demo/tree/workshop-1/workshop).

Note: Download the latest XL CLI: [8.5.0-alpha.2](https://s3.amazonaws.com/xl-cli/bin/8.5.0-alpha.2/darwin-amd64/xl). 

Tell [Hes](mailto:hsiemelink@xebialabs.com) if you run into trouble. The Dev ♥︎ team is working on a proper release process in the meanwhile, so we won't have issues here.

### Run XL Release and Jenkins

#### Start Docker
Start docker from the `demo/JenkinsWorld` directory

    $ cd demo/JenkinsWorld
    $ docker-compose up -d

This will start

* XL Release on http://localhost:5516.
* XL Deploy on http://localhost:4516
* Jenkins on http://localhost:8080
* Docker proxy for local XL Deploy deployments
* XL-CLI task container to link XL Release to XL Deploy

Use admin/admin credentials for XL Release, XL Deploy and Jenkins.

### Configure XL Release templates

Run the following script that will add the templates by calling `xl apply -f` in the right order.

    ./setup.sh

Check XL Release for the Jenkins World folder.

## Configure Jenkins

Create a folder called **Cool Store** in Jenkins.

In order to do this, you first need to [create a personal access token in GitHub](https://github.com/settings/tokens).

You can use this token as a credential in Jenkins.

Import the following projects from GitHub as multibranch projects in the **Cool Store** folder

* [demo-address-book](https://github.com/xebialabs/demo-address-book) as "Address book"
* [demo-shopping-cart](https://github.com/xebialabs/demo-shopping-cart) as "Shopping cart"
* [demo-wish-list](https://github.com/xebialabs/demo-wish-list) as "Wish list"

Here's an example of the parameters:

![Jenkins Branch Source](doc/jenkins-branch-source.png)

## Set up release train

You should have the following folder structure in XL Release:

    Cool Store
    +-- Address book
    +-- Shopping cart
    +-- Wish list
    JenkinsWorld
    Samples & Tutorials
    Set up

Run a release from the template **Set up/Set up Cool Store release train**

This will create several releases and link them together using Gate tasks.

You will end up with something like this on the Relationship view of the **Cool Store September delivery** release:

Wait on the **Jenkins has GitHub projects** task.

Go to the **Cool Store September delivery** and select the relationship viewer. 

You should see something like this:

![Jenkins Branch Source](doc/cool-store-relations-up-to-features.png)


### Import Jenkins projects

Continue the Set up release and the release train will be connected to the Release train.

Kick off a manual build in Jenkins of **Address book/COOL-113**

This should create a release in XL Release.

Go to the **Cool Store/Address book** folder and select the **Releases** tab. The Jenkins build should appear here. Make sure to select active releases.

![Jenkins Branch Source](doc/jenkins-build-running.png)

Clicking on the build will show the stages:

![Shadow pipelin in XL Release](doc/jenkins-shadow-pipeline.png)

This corresponds with the BlueOcean view in Jenkins:

![Jenkins Blue Ocean](doc/jenkins-blue-ocean.png)

## Set up dashboards

Clone https://github.com/Hes-Siemelink/yay and run `python setup.py install`. (This is a utility to run YAML scripts to chain REST calls.)

Create a file `~/.yay/default-variables.yaml` with the following contents:

    xlreleaseUrl: http://admin:admin@localhost:5516
    
Run `./insert.sh`

Go to the Cool Store folder. It should display a dashboard.

![Cool Store dashboard](doc/cool-store-dashboard.png)
