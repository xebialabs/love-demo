# REST-o-rant on AWS EC2 Container Service (ECS) with Fargate

This demos show you how to deploy to ECS with XL Deploy.

## Prerequisites
* AWS Command Line Tools
* Python 3.6 or up

## Step 1 - Configure AWS in XL Deploy

Make sure you have setup the AWS command line interface installed and configured correctly as per [these instructions](https://docs.aws.amazon.com/cli/latest/userguide/tutorial-ec2-ubuntu.html#configure-cli).


This demo will not use the AWS command line interface itself, but will use the [credentials and configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html) in the `~/.aws/credentials` and `~/.aws/config` files:


Once you've configured the AWS command line interface, use the `awsconfig2xld.py` script in the `config` directory to create XL YAML files that will create the AWS environment in XL Deploy.

```
$ config/awsconfig2xld.py > /tmp/AWSConfig.yaml
```

Now send this file to XL Deploy using

```
$ xl apply -f /tmp/AWSConfig.yaml
```

## Step 2 - Import the REST-o-rant YAML definition:

Import the REST-o-rant ECS/Fargate cluster definition for AWS into XL Deploy:

```
$ xl apply -f demo/ecs/rest-o-rant-ecs-fargate-cluster.yaml
$ xl apply -f demo/ecs/rest-o-rant-ecs-service.yaml
$ xl apply -f demo/ecs/rest-o-rant-ecs-pipeline.yaml
```

## Step 3 - Start the release pipeline

1. Go to the XL Release UI running on http://localhost:5516.

2. Go to the Templates page under the Design tab.

3. Start a release from the "REST-o-rant on ECS" template.

4. Follow the instructions.
