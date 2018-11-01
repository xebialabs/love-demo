# Approach

Taking into account that devops-as-code provides convenient wrapper for *NIX and Windows systems, it is very easy to using together with different CI tools.

It is very easy to integrate devops-as-code into your git flow in Azure DevOps you should do the following:

1) Add wrappers to your project. You can either copy/paste them from another project, or execute `xl wrapper` command in the root of your project to generate them.
2) Define devops-as-code YAML in your project's directory.
3) On DevOps Azure you can define your build pipeline using a YAML file, normally this YAML file is called `azure-pipeline.yml` and should be located in the root of the repo.
4) To make use of XL-Client you can define a pipeline with a `bash/script` step, depending on the OS to use.
On Windows you should use a `script` step. In case of Linux you should use a `bash` step.
    * Linux/Mac:
        ```yaml
          ....
          - bash: |
             ./xlw apply -f xebialabs.yaml
        ```
    * Windows:
        ```yaml
          ....
          - script: |
             xlw apply -f xebialabs.yaml
        ```
5) If you want to use external values, you can add environment variables or use variables inside the pipeline.

# Dealing with XLD/XLR credentials

There are many ways how you can specify XLD/XLR username and password when you use devops-as-code:

**Using `<USER_HOME>/.xebialabs/config.yaml`:**
```yaml
xl-deploy:
  password: admin
  url: http://localhost:4516
  username: admin
xl-release:
  password: admin
  url: http://localhost:5516
  username: admin
```

---
**Using inline command parameters:**
```bash
./xlw apply -v -f xld.yaml --xl-deploy-username admin --xl-deploy-password qwerty

./xlw apply -v -f xlr.yaml --xl-release-username admin --xl-release-password qwerty
```

---
**Using environment variables.**
1. On each `bash / script` step you can define different environment variables:<br>
    Define `XL_RELEASE_URL` for `XLR`
    ```yaml
    .....
    - bash: |
       ./xlw apply -f xebialabs.yaml
      displayName: 'Bash Script'
      continueOnError: true
      env:
        XL_RELEASE_URL = "http://xl-release:5516"
    ```

2. With the help of Variables:<br>
    Define `XL_RELEASE_USERNAME` for `XLR`<br>
    This approach is convenient if you'd like to use variables from Azure DevOps build pipeline.
    ```yaml
    .....
    - bash: |       
       ./xlw apply -f xebialabs.yaml
      displayName: 'Bash Script'
      continueOnError: true
      env:
        XL_RELEASE_USERNAME: $(xlr.username)
    ```
    
# Working with usernames and passwords

Devops-as-code allows you to include in your yaml files with the help of value injection.
Imagine, that you'd like to dynamically inject `username` and `password` into such yaml file:

```yaml
apiVersion: xl-deploy/v1beta1
kind: Infrastructure
spec:
- name: TomcatHostAsCode
  type: overthere.SshHost
  os: UNIX
  connectionType: SUDO
  address: 192.168.55.11
  port: 21
  username: !value tomcat_username
  password: !value tomcat_password
```

You can specify the values using xlvals files. Please use the extension `.xlvals`, for example put the following values in a file called `secrets.xlvals`:

```properties
tomcat_username=admin
tomcat_password=424242
```

Please make sure to not check in value files that contain sensitive information into version control. The XL Cli searches for value files in `<USER_HOME>/.xebialabs` and in the folder the yaml file is located. If you keep the xlvals file in the project directory, you can add it to the gitignore to prevent the file from being checked in.

---
**Using inline command parameters:**
```bash
./xlw apply -v -f host.yaml --values=tomcat_username=admin --values=tomcat_password=424242

# passing multiple values
./xlw apply -v -f host.yaml --values=tomcat_username=admin --values=order=1 --values=tomcat_password=424242 --values=passphrase=secret
```

---
**Using environment variables.**
Any environment variable that starts with `XL_VALUE_` will be passed devops-as-code command as a value respectively.<br>

_**Please notice, that variable names are case sensitive**_

```yaml
- bash: |
   # Write your commands here
   
   # Use the environment variables input below to pass secret variables to this script
   
   sleep 120
   
   export DOCKER_PORT=$(docker port gitops_xl-release_1 5516 | awk -F: '{print $2}')
   
   ./xlw apply -f xebialabs.yaml --xl-release-url http://localhost:$DOCKER_PORT 
  displayName: 'Bash Script'
  continueOnError: true
  env:
    XL_VALUE_RELEASE_NAME: Test Release
    XL_VALUE_BUILD_NUMBER: $(Build.BuildId)
```

# Azure Key Vault integration

It is possible to insert values from Azure Key Vault.

Just follow these simple steps:
* Create a new `Azure Key Vault` in your [Azure Account](https://portal.azure.com)
* Copy your subscription ID from the `Azure Key Vault` previously created
* Configure a new Azure Resource Manager in `Service Connections` in your `Project Settings`
* Add a `Azure Key Vault` step to the pipeline
* Configure in the step your subscription and also the vault that you want to use
* After that configuration, all the **following steps** can use secrets stored in the **Azure Key Vault**  as a Variable.
E.g: If in your vault you have a secret with key `mySecret` you can access it using `$(mySecret)`
* Inject data from Azure key vault into `XL_VALUE_` environment variables:
    ```yaml
    - bash: |
      # Write your commands here
       
      # Use the environment variables input below to pass secret variables to this script
       
      export DOCKER_PORT=$(docker port gitops_xl-release_1 5516 | awk -F: '{print $2}')
       
      ./xlw apply -f xebialabs.yaml --xl-release-url http://localhost:$DOCKER_PORT 
      displayName: 'Bash Script'
      continueOnError: true
      env:
        XL_VALUE_RELEASE_NAME: $(testSecret)
        XL_VALUE_BUILD_NUMBER: $(testValue)
    ```
    
