# JenkinsWorld demo

This is the setup for the JenkinsWorld 2018 demo in San Francisco.

## Demo Set up

### Set up Docker & CLI

First, set up Docker and the XL client using the first step of the [DevOps as Code workshop](https://github.com/xebialabs/devops-as-code-demo/tree/workshop-1/workshop).

Note: the `xl` client used there is an older version. Tell [Hes](mailto:hsiemelink@xebialabs.com) if you run into trouble. The Dev ♥︎ team is working on a proper release process in the meanwhile, so we won't have issues here.

### Run XL Release and Jenkins

#### Jenkins pipeline radar
Check out [xlr-jenkins-pipeline-radar-plugin](https://github.com/xebialabs/xlr-jenkins-pipeline-radar-plugin/) into `~/Code`. (This weird step will disappear soon)

#### Start Docker
Now start docker from the `demo/JenkinsWorld` directory

```
$ cd demo/JenkinsWorld
$ docker-compose up -d
```

This will start

* XL Release on http://localhost:5516
* XL Deploy on http://localhost:4516
* Jenkins on http://localhost:8080
* Docker proxy for local XL Deploy deployments
* XL-CLI task container to link XL Release to XL Deploy

### Configure XL Release templates

Run the following script that will add the templates by calling `xl apply -f` in the right order.

```
./setup.sh
```

Check XL Release for the Jenkins World folder.

### Clean up the templates

There are still some rough edges in the YAML import.

Run a release from the template **Manual Demo Setup** in the **Set up** folder.

_This is work in progress_

## Configure Jenkins

Create a folder called **Cool Store** in Jenkins.

Import the following projects from GitHub as multibranch projects in the **Cool Store** folder

* [demo-address-book](https://github.com/xebialabs/demo-address-book)
* [demo-shopping-cart](https://github.com/xebialabs/demo-shopping-cart)
* [demo-wish-list](https://github.com/xebialabs/demo-wish-list)

## Import projects into XL Release

Create the following folder structure in XL Release

```
Cool Store
+-- Address book
+-- Shopping cart
+-- Wish list
```

Use the template **JenkinsWorld/Import Jenkins Pipelines** to import the projects from Jenkins. You need to run it for each of the three subprojects, but not for the main Cool Store project.

For the **Master template** variable, fill in `JenkinsWorld/Track Jenkins pipeline`.

Templates will be created in the folders you created above.

### Dry run

Enable the trigger on any tracker template and kick off a manual build in Jenkins.

This should create a release in XL Release.

## Set up Release trains

...

