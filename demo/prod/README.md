This file describes how to run the demo for Team Developer Love sprint 2.

## Step 1 - ECS prerequisites and setup

This demo builds on the full `ecs` demo. Please follow [its steup document](../ecs/README.md) up to and including step 1.

## Step 2 - Start and configure the production XL DevOps Platform system


1. Start the production XL DevOps Platform system
```
$ cd .../as-code-demo/demo/prod
$ docker-compose up -d
```

2. Wait until both XL Deploy and XL Release have started up. They can be accessed as follows:
  * XL Deploy: http://localhost:14516/ (username: `admin`, password: `3dm1n`)
  * XL Release: http://localhost:15516/ (username: `admin`, password: `3dm2n`)

3. Run the additional setup that will create a user called `kate` (password: `k3t3`) with limited privileges.
```
$ export XL_DEPLOY_CLI_CONFIG=.../xl-deploy-8.1.0-cli
$ ./setup-prod
```

## Step 3 - Connect to the "Dev" instance of the XL DevOps Platform

```
$ rm ~/.xebialabs/config.yaml
$ unset XL_CONFIG
```

## Step 4 - Generate and apply the YAML files for the REST-o-rant application (see also the demo for Team Developer Love sprint 1)

```
$ ../../config/awsconfig2xld.py > /tmp/AWSConfig.yaml
$ xl apply -f /tmp/AWSConfig.yaml
$ xl apply -f ../ecs/rest-o-rant-ecs-fargate-cluster.yaml
$ xl apply -f ../ecs/rest-o-rant-ecs-service.yaml
$ xl apply -f ../ecs/rest-o-rant-ecs-pipeline.yaml
```

## Step 6 - Configure the CLI to connect to the "Prod" instance of the XL DevOps platform

```
$ export XL_CONFIG=`pwd`/prod-config.yaml
```
  
## Step 7 - Import AWS credentials to the home directory configured for the user `kate`

```
$ ../../config/awsconfig2xld.py > /tmp/AWSConfig.yaml
$ xl apply -f /tmp/AWSConfig.yaml
```

## Step 8 - Apply YAML files to the the home directory configured for the user `kate`
```
$ xl apply -f ../ecs/rest-o-rant-ecs-fargate-cluster.yaml
$ xl apply -f ../ecs/rest-o-rant-ecs-service.yaml
$ xl apply -f ../ecs/rest-o-rant-ecs-pipeline.yaml
```
