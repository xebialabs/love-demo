# JenkinsWorld demo

This is the setup for the JenkinsWorld demo, originally shown at the JenkinsWorld 2018 in San Francisco.

_For the stable version of the demo please use the [JenkinsWorld-SF](https://github.com/xebialabs/devops-as-code-demo/tree/JenkinsWorld-SF/demo/JenkinsWorld) branch and follow the instructions of the README in that branch._


## Demo Set up

### Set up Docker & CLI

You'll need to have Docker installed on your machine before you begin:

* Mac: https://docs.docker.com/docker-for-mac/
* Windows: https://docs.docker.com/docker-for-windows/
* Linux: Refer to the instructions for your Linux distribution on how to install Docker

Download the latest XL CLI: [8.5.0-alpha.2](https://s3.amazonaws.com/xl-cli/bin/8.5.0-alpha.2/darwin-amd64/xl). 


### Run XL Release and Jenkins

#### Configure passwords

Configure third-party passwords before starting XL Release.

##### Fortify On Demand, Checkmarx and JIRA

Open or create `~/.xebialabs/config.yaml`, paste in the following section and configure the passwords by copying them from LastPass.

	secrets:
	  checkmarx.password: INSERT PASSWORD FROM LASTPASS
	  fortify.password: INSERT PASSWORD FROM LASTPASS
	  jira.password: INSERT PASSWORD FROM LASTPASS
	values:
	  checkmarx.url: https://xl-chkmarx-poc.xebialabs.com/
	  checkmarx.user: xl-admin
	  fortify.url: https://api.emea.fortify.com/
	  fortify.user: xebialabs\deployit-dev
	  jira.url: https://xebialabs.atlassian.net/
	  jira.user: xlr-jira-testuser@xebialabs.com

##### XL Impact

Find the password for `demo.xebialabs.io` in LastPass. (Hint: search for 'demo' in LastPass)

Paste it in the following line of `xl-impact/xl-release.conf`:

    password="INSERT PASSWORD FROM LASTPASS AND DO NOT COMMIT PLEASE"

#### Start Docker

Start the VPN client (Cisco AnyConnect) to be able download the latest XL Release and XL Deploy versions.

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


## Configure Jenkins

Create a folder called **Cool Store** in Jenkins.

For the following steps you need to [create a personal access token in GitHub](https://github.com/settings/tokens).

Give the token the following permissions:

* `repo`
* `admin:repo_hook`
* `user`

You can use this token as a credential in Jenkins. Use the **Add** button on the  Branch Source section below to add it to Jenkins.

Import the following projects from GitHub as separate multibranch projects in the **Cool Store** folder. Note that the job names are case sensitive!

* [demo-address-book](https://github.com/xebialabs/demo-address-book) as `Address book`
* [demo-shopping-cart](https://github.com/xebialabs/demo-shopping-cart) as `Shopping cart`
* [demo-wish-list](https://github.com/xebialabs/demo-wish-list) as `Wish list`

Here's an example of the parameters:

![Jenkins Branch Source](doc/jenkins-branch-source.png)

_Note: Jenkins configuration is persistent, so you don't have to do this again after doing docker-compose down & up._

## Set up release train

Run the following script that will add the templates by calling `xl apply -f` in the right order.

    ./setup.sh

You should have the following folder structure in XL Release:

    Cool Store
    +-- Address book
    +-- Shopping cart
    +-- Wish list
    JenkinsWorld
    Samples & Tutorials
    Set up

Now go to the [My tasks](http://localhost:5516/#/tasks?has_filter&active&assignedToMe&assignedToMyTeams) view and complete the **Jenkins has GitHub projects** task. (You may need to wait a bit and refresh if you are fast.)

The **Set up Cool Store demo** creates several releases and link them together using Gate tasks.

Go to the **Cool Store September delivery** and select the relationship viewer. 

You should see something like this:

![Jenkins Branch Source](doc/cool-store-relations-up-to-features.png)


### Import Jenkins projects

Go back to Jenkins and kick off a manual build in Jenkins of [Address book/COOL-113](http://localhost:8080/job/Cool%20Store/job/Address%20book/)

This should create a release in XL Release.

Go to the **Cool Store/Address book** folder and select the **Releases** tab. The Jenkins build should appear here. Make sure to select active releases.

![Jenkins Branch Source](doc/jenkins-build-running.png)

Clicking on the build will show the stages:

![Shadow pipelin in XL Release](doc/jenkins-shadow-pipeline.png)

This corresponds with the BlueOcean view in Jenkins:

![Jenkins Blue Ocean](doc/jenkins-blue-ocean.png)

Now manually trigger a build for *all* projects in all folders (exclude the 'master' builds) to seed the data in XL Release.

Note that the Jenkinsfiles are configured that to fail intermittently. So your job may succeed or fail.

## Set up dashboards

### Pre-requistes

* Python 3

On Macos, the easiest way seems to be:

	$ brew install python
 	$ alias python='python3'

* `pip3 install pyyaml`
* Turn on the VPN (Cisco AnyConnect) to be able to connect to Checkmarx server.

### Run scripts

To add the dashboards we need to call internal APIs. We will use the Yay, a utility I wrote to run YAML scripts that chain REST calls. 

Clone and install Yay in another directory. Use the **JenkinsWorld** tag.

	$ git clone https://github.com/Hes-Siemelink/yay
	$ cd yay
	$ git checkout JenkinsWorld
	$ python setup.py install

Create a file `~/.yay/default-variables.yaml` with the following contents:

    xlreleaseUrl: http://admin:admin@localhost:5516
    
Run `./insert.sh`

Go to the Cool Store folder. It should display a list with one dashboard.

![Cool Store dashboard](doc/cool-store-dashboard-list.png)

Click on **Cool Store Dashboard** to reveal the dashboard.

![Cool Store dashboard](doc/cool-store-dashboard.png)

## Stopping

The following will kill the demo

    docker-compose down
    
Note that this will wipe XL Release and XL Deploy, but the data in Jenkins will remain intact. The next time you start the demo you need to do all configuration steps except the Jenkins configuration.

## Set up XL Deploy

Not needed for the XL Release demo flow, but if you want to show how XL Deploy works follow these steps.

These steps can be done independently if you just want to show XL Deploy.

Set up XL Deploy server in XL Release

	JenkinsWorld        $ cd ../..
	devops-as-code-demo $ xl apply -f config/configure-xl-devops-platform.yaml 

Set up environment and packages in XL Deploy

	devops-as-code-demo $ xl apply -f workshop/exercise-2/docker-environment.yaml 
	devops-as-code-demo $ xl apply -f workshop/exercise-4/rest-o-rant-docker.yaml
	devops-as-code-demo $ xl apply -f workshop/exercise-5/rest-o-rant-docker-pipeline.yaml 


You can now deploy **rest-o-rant-api-docker** followed by **rest-o-rant-web-docker** to the **Local Docker Enginge** environment, or use the pipeline in XL Release.


# Demo flow

## Starting screens

Go to **Cool Store** folder; select **Releases** and open **Cool Store September delivery**. Select the **Relationship** screen. Check **Releases label** and uncheck **Relations label**. 

This is the starting point of the demo in XL Release.

![Jenkins Branch Source](doc/cool-store-relations-up-to-features.png)

Open another browser tab and open a Blue Ocean view on a completed pipeline so you can easily switch to it.

![Jenkins Blue Ocean](doc/jenkins-blue-ocean.png)

## 1. Overview

Using the relationship view, explain that we have a sample release for the product **Cool Store**, that is scheduled for September. The Cool Store release consists of the components **Address book**, **Shooping cart** and **Wish list**. 

Each component has a set of features being implemented that are denoted by thier **COOL** ticket number.

Finally we have the Jenkins pipelines that feed into the feature delivery.

## 2. Jenkins pipelines
Click on a Jenkins Pipeline in XL Release and explain that the phases and tasks correspond one-on-one to the stages in Jenkins. Quickly switch to Jenkins Blue Ocean view to show this. (Tip: Use the first two tabs in your browser and use Command-1 and Command-2 keyboard shortcuts to quickly switch between tabs)

Explain that we here XL Release is an observer of the pipeline. We show the status and use the data from Jenkins to do Release Value Stream Mapping and compliance analysis.

Go back to the relationship overview (Just hit back on the browser) and tell that the when the pipeline completes, it feeds into the feature delivery process. Click on a COOL-xxx release and show phases and tasks in XL Release, executed form top to bottom, left to right.

## 3. Feature delivery

Now we are leaving the Jenkins domain and start to tap into the higher level process. We start to involve more people, the Security Officer for example, who would normally not go into Jenkins to check compliance.

After the pipeline completes with success, we can do security gates (first phase), integrating with Fortify and BlackDuck for example. 

The second phase shows a QA procedure. QA people don't live in Jenkins, they use ServiceNow or JIRA. We integrate with both and in this example we use JIRA. We create a JIRA ticket from XL Release, and wait until the QA person picks it up. Then we deploy the artifact using XL Deploy or any other deployment solution.

We can ran both automated tests and track manual testing. For example, somebody has to look into the feature to see if it works well, is the CSS properly aligned, etc. If that has been done and QA gives the OK we have a manual approval here.


XL Release can do both fully automated pipelines, fully manually deliveries and anything in between. This helps you in your DevOps transformation because you can start using it at any point, giving the benefit of tracking the process and dashboarding on a single pane of glass. This way it helps you to identify where you need to improve the process. You can seamlessly convert manual steps to automated once. Show Change Task type.

Finally in this part of the delivery, if everything is OK the pull request is automatically merged and we move up the the component level.

## 4. Software delivery

As you can imagine, the component delivery has a similar process and I will not jump into it here. It is interesting to take a look at the complete Software delivery.

Click to the **Cool Store September delivery**.

Here, we see a similar procedure, we have some QA on acceptance (second phase), but all of a sudden (third phase) Product Marketing is involved. They need to start writing content, get the blogs out, so they are being sent an email.

## 5. Dashboarding

Go to **Cool Store** folder and click on **Cool Store Dashboard**.

Since we track everything in XL Release we can do reporting on all levels. 

For example, here you will see the high level reports: release duration and automation. On this tile (top right) you will see manual is yellow and purple is automated. So far we have automated two thirds, sounds pretty good. But below it you see the time spent, that is all yellow -- all manual work, that is where the money goes.

Go to **Address book** folder and click on **Pipeline Dashboard**. (Or another component folder that has the Release Value Stream mapping tile populated).

This is reporting on the Jenkins level, here we do a Release Value Stream Mapping on the Jenkins pipeline. Look at the red numbers, this means that this stage took the most time.

Then we have the integrations with Fortify and Checkmarx, so you have high level information if you are adhering to security standards, again on a single piece of glass.

This concludes the mini-demo.

## 6. More...

* Show **XL Impact** and discuss KIP-based DevOps transformation improvements.
* Show **XL Deploy**. Deploy **rest-o-rant-api-docker** followed by **rest-o-rant-web-docker** to the **Local Docker Enginge** environment.
