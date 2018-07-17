# NOT WORKING YET -- AWS Provisioning

Creates AWS infrastructure and deploys Rest-o-Rant application to it.

*THIS DEMO NEEDS SUPPORT FOR ARTIFACT UPLOAD IN XL CLIENT*


## Step 1. Configure AWS in XL Deploy

Make sure you have access to an AWS environment.

Create a file `~/.xl-config/secrets.yaml`.

Specify your AWS credentials in this file. You need to define the following entries:

```
aws.keypair:       [Name of your keypair]
aws.keypair.file:  [Location of your PEM file]
aws.access.key:    [Access key for AWS]
aws.access.secret: [Secret for AWS]
```

Also create a file `~/.xl-config/default-values.yaml`:

```
aws.region: eu-west-1
```


Use the `resolve-secrets.py` script in the `config` directory to create XL YAML files that will create the AWS environment in XL Deploy.

	python config/resolve-secrets.py > AWS-Environment.yaml
	
Now send this file to XL Deploy using

	xl apply -f AWS-Environment.yaml
	
In XL Deploy, run 'check connection' on Infrastructure/AWS Cloud to see if your credentials have been imported correctly.
	
## Step 2. Import the Rest-o-rant application and AWS provisioning

Use the following command to import the Rest-o-rant application with AWS provisioning into XL Deploy.

	xl apply -f demo/aws-provisioning/Rest-o-Rant-Package.yaml

## Step 3. Run the pipeline in XL Release

Create a template in XL Release using

	xl apply -f demo/aws-provisioning/Rest-o-Rant-Pipeline.yaml

Now go to the XL Release UI running on http://localhost:5516.
Go to **Design > Templates** and locate the **AWS Provisioning Demo** template.

Create a new release from the template, start it and follow the release flow.
	
	




