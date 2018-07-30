This directory contains the `ecs` demo scenario split up into parts for
the demo of Team Developer Love sprint number 1.

## Step 0 - Configure AWS in XL Deploy

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


## Step 1 - Provision an ECS cluster and deploy an ECS service

1. Apply the YAML files that define the ECS cluster and service:
```
$ xl apply -f demo/ecs-in-steps/step-1/rest-o-rant-ecs-fargate-cluster.yaml
$ xl apply -f demo/ecs-in-steps/step-1/rest-o-rant-ecs-service.yaml
```

1. Provision the cluster by deploying `Applications/AWS/rest-o-rant-ecs-fargate-cluster/1.0` to `Environments/AWS`
1. Deploy the service by deploying `Applications/AWS/rest-o-rant-ecs-service/1.0` to `Environments/AWS`

## Step 2 - Add a container  to the ECS service

1. Apply the new YAML file that defines the updated ECS service:
```
$ xl apply -f demo/ecs-in-steps/step-2/rest-o-rant-ecs-service.yaml
```

1. Update the service by redeploying `Applications/AWS/rest-o-rant-ecs-service/1.0` to `Environments/AWS`

## Step 3 - Add a port mapping to the ECS service

1. Apply the new YAML file that defines the updated ECS service:
```
$ xl apply -f demo/ecs-in-steps/step-3/rest-o-rant-ecs-service.yaml
```

1. Update the service by redeploying `Applications/AWS/rest-o-rant-ecs-service/1.0` to `Environments/AWS`

## Step 4 - Add a simple pipeline

1. Undeploy `rest-o-rant-ecs-service/1.0` from `Environments/AWS`
1. Apply the YAML file that defines the pipeline:
```
$ xl apply -f demo/ecs-in-steps/step-4/rest-o-rant-ecs-pipeline.yaml
```

1. Run the pipeline from XL Release.


## Step 5 - Add proviosing and a simpler manual step to the pipeline

1. Deprovision the ECS cluster by undeploying `rest-o-rant-ecs-fargate-cluster/1.0` from `Environments/AWS`
1. Apply the new YAML file that defines the updated pipeline:
```
$ xl apply -f demo/ecs-in-steps/step-4/rest-o-rant-ecs-pipeline.yaml
```

1. Run the pipeline from XL Release once more.
