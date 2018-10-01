# JenkinsWorld demo

This is the setup for the JenkinsWorld 2018 demo in San Francisco.

## Demo Set up

### Set up Docker & CLI

First, set up Docker and the XL client using the first step of the [DevOps as Code workshop](https://github.com/xebialabs/devops-as-code-demo/tree/workshop-1/workshop).

Note: Download the latest XL CLI: [8.5.0-alpha.2](https://s3.amazonaws.com/xl-cli/bin/8.5.0-alpha.2/darwin-amd64/xl). 

Tell [Hes](mailto:hsiemelink@xebialabs.com) if you run into trouble. The Dev ♥︎ team is working on a proper release process in the meanwhile, so we won't have issues here.

### Run XL Release and Jenkins

#### Configure passwords

Configure third-party passwords before starting XL Release.

##### XL Impact

Find the password for `demo.xebialabs.io` in LastPass. (Hint: search for 'demo' in LastPass)

Paste it in the following line of `xl-impact/xl-release.conf`:

    password="INSERT PASSWORD FROM LASTPASS AND DO NOT COMMIT PLEASE"

##### Fortify, Checkmarx and JIRA

Open `templates/shared_configuration.yaml` and insert passwords from LastPass.

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

Now manually trigger a build for *all* projects in all folders (exclude the 'master' builds) to seed the data in XL Release.

## Set up dashboards

### Pre-requistes

* Python 3
* `pip3 install requests`
* `pip3 install jsonpath_rw`


### Run scripts

Clone https://github.com/Hes-Siemelink/yay and run `python setup.py install`. (This is a utility to run YAML scripts that chain REST calls. You need Python 3 to run it.)

Create a file `~/.yay/default-variables.yaml` with the following contents:

    xlreleaseUrl: http://admin:admin@localhost:5516
    
Run `./insert.sh`

Go to the Cool Store folder. It should display a dashboard.

![Cool Store dashboard](doc/cool-store-dashboard.png)

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

Go to **Cool Store** folder.

Since we track everything in XL Release we can do reporting on all levels. 

For example, here you will see the high level reports: release duration and automation. On this tile (top right) you will see manual is yellow and purple is automated. So far we have automated two thirds, sounds pretty good. But below it you see the time spent, that is all yellow -- all manual work, that is where the money goes.

Go to **Address book** folder. (Or another component that has the Release Value Stream mapping tile populated).

This is reporting on the Jenkins level, here we do a Release Value Stream Mapping on the Jenkins pipeline. Look at the red numbers, this means that this stage took the most time.

Then we have the integrations with Fortify and Checkmarx, so you have high level information if you are adhering to security standards, again on a single piece of glass.

This concludes the mini-demo.

## 6. More...

* Show **XL Impact** and discuss KIP-based DevOps transformation improvements.
* Show **XL Deploy**.