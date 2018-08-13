This directory contains the `ecs` demo scenario split up into parts for
the demo of Team Developer Love sprint number 1.

## Step 1 - Prerequisites and setup

The prerequisites and setup for this demo are identical to the full `ecs` demo. Please follow [the corresponding README document](../ecs/README.md) up to and including step 1.

## Step 2 - Provision an ECS cluster and deploy an ECS service

1. Apply the YAML files that define the ECS cluster and service:
```
$ xl apply -f demo/ecs-in-steps/step-4/rest-o-rant-ecs-fargate-cluster.yaml
$ xl apply -f demo/ecs-in-steps/step-4/rest-o-rant-ecs-service.yaml
```

1. Provision the cluster by deploying `Applications/AWS/rest-o-rant-ecs-fargate-cluster/1.0` to `Environments/AWS`
1. Deploy the service by deploying `Applications/AWS/rest-o-rant-ecs-service/1.0` to `Environments/AWS`

## Step 3 - Add a container to the ECS service

1. Apply the new YAML file that defines the updated ECS service:
```
$ xl apply -f demo/ecs-in-steps/step-5/rest-o-rant-ecs-service.yaml
```

1. Update the service by redeploying `Applications/AWS/rest-o-rant-ecs-service/1.0` to `Environments/AWS`

## Step 4 - Add a port mapping to the ECS service

1. Apply the new YAML file that defines the updated ECS service:
```
$ xl apply -f demo/ecs-in-steps/step-6/rest-o-rant-ecs-service.yaml
```

1. Update the service by redeploying `Applications/AWS/rest-o-rant-ecs-service/1.0` to `Environments/AWS`

## Step 5 - Add a simple pipeline

1. Undeploy `rest-o-rant-ecs-service/1.0` from `Environments/AWS`
1. Apply the YAML file that defines the pipeline:
```
$ xl apply -f demo/ecs-in-steps/step-7/rest-o-rant-ecs-pipeline.yaml
```

1. Run the pipeline from XL Release.


## Step 6 - Add provisioning and a simpler manual step to the pipeline

1. Deprovision the ECS cluster by undeploying `rest-o-rant-ecs-fargate-cluster/1.0` from `Environments/AWS`
1. Apply the new YAML file that defines the updated pipeline:
```
$ xl apply -f demo/ecs-in-steps/step-8/rest-o-rant-ecs-pipeline.yaml
```

1. Run the pipeline from XL Release once more.
