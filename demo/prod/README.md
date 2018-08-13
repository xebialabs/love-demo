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

4.  Configure the CLI to user these credentials:

```
$ export XL_CONFIG=`pwd`/prod-config.yaml
```

## Step 3 - Import AWS credentials for the developer user

```
$ ../../config/awsconfig2xld.py > /tmp/AWSConfig.yaml
$ xl apply -f /tmp/AWSConfig.yaml
```

## Step 4 - import ECS files into the right home directories:
```
$ xl apply -f ../ecs/rest-o-rant-ecs-fargate-cluster.yaml
$ xl apply -f ../ecs/rest-o-rant-ecs-service.yaml
$ xl apply -f ../ecs/rest-o-rant-ecs-pipeline.yaml
```
