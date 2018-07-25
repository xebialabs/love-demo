# Rest-o-rant on Kubernetes

This demos show you how to run a Kubernetes pipeline in XL Release and XL Deploy.

## Prerequisites
* Minikube
* Python 3.6 or up


## Step 1. Configure Minikube in XL Deploy

Make sure you have a running minikube environment locally.

Use the `kubeconfig2xld.py`  in the `config` directory to create XL YAML files that will create the Kubernetes environment in XL Deploy.

```
$ config/kubeconfig2xld.py > /tmp/KubeConfig.yaml
```

Now send this file to XL Deploy using

```
$ xl apply -f /tmp/KubeConfig.yaml
```

## Step 2. Import the Rest-o-rant application

Use the following command to import the Rest-o-rant application or Kubernetes into XL Deploy.

```
$ xl apply -f demo/k8s/k8s-rest-o-rant-package.yaml
```

## Step 3. Run the pipeline in XL Release

Create a template in XL Release using

```
$ xl apply -f demo/k8s/k8s-rest-o-rant-pipeline.yaml
```

Now go to the XL Release UI running on http://localhost:5516.
Go to **Design > Templates** and locate the **Rest-o-rant Kubernetes** template.

Create a new release from the template, start it and follow the release flow.
