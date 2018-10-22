# Approach

Taking into account that devops-as-code provides convenient wrapper for *NIX and Windows systems, it is very easy to using together with different CI tools.

To integrate devops-as-code into your git flow, please follow these simple steps:

1) Add wrappers to your project. You can either copy/paste them from another project, or execute `xl wrapper` command in the root of your project to generate them.
2) Define devops-as-code YAML in your project's directory.  
3) Define `sh / bat` step in your `Jenkinsfile` and point to your devops-as-code YAML file(s)
    * Windows:
        ```groovy
          ....
          stages {
              stage("Apply xebialabs.yaml") {
                  steps {
                      bat "xlw.bat apply -v -f xebialabs.yaml"
                  }
              }
          }
        ```
    * Linux/Mac:
        ```groovy
          ....
          stages {
              stage("Apply xebialabs.yaml") {
                  steps {
                      sh "./xlw apply -v -f xebialabs.yaml"
                  }
              }
          }
        ```
4) Tweak `bat/sh` calls by adding parameters you need.

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
1. With the help of USERNAME/PASSWORD fields:<br>
    Define `XL_DEPLOY_USERNAME, XL_DEPLOY_PASSWORD` for `XLD` and `XL_RELEASE_USERNAME, XL_RELEASE_PASSWORD` for `XLR`
    ```groovy
    pipeline {
        agent any
        environment {
            XL_DEPLOY_URL = "http://xl-deploy:4516"
            XL_DEPLOY_USERNAME = "${env.XL_DEPLOY_CREDENTIALS_USR}"
            XL_DEPLOY_PASSWORD = "${env.XL_DEPLOY_CREDENTIALS_PSW}"
    
            XL_RELEASE_URL = "http://xl-release:5516"
            XL_RELEASE_USERNAME = "${env.XL_RELEASE_CREDENTIALS_USR}"
            XL_RELEASE_PASSWORD = "${env.XL_RELEASE_CREDENTIALS_PSW}"
        }
    
        stages {
            stage("Apply xebialabs.yaml") {
                steps {
                    sh "./xlw apply -v -f xebialabs.yaml"
                }
            }
        }
    }
    ```

2. With the help of CREDENTIALS field:<br>
    Define `XL_DEPLOY_CREDENTIALS` for `XLD` and `XL_RELEASE_CREDENTIALS` for `XLR`<br>
    This approach is convenient if you'd like to use jenkins credentials provider.
    ```groovy
    pipeline {
        agent any
        environment {
            XL_DEPLOY_URL = "http://xl-deploy:4516"
            XL_DEPLOY_CREDENTIALS = credentials("xld-credentials")
    
            XL_RELEASE_URL = "http://xl-release:5516"
            XL_DEPLOY_CREDENTIALS = credentials("xlr-credentials")
        }
    
        stages {
            stage("Apply xebialabs.yaml") {
                steps {
                    sh "./xlw apply -v -f xebialabs.yaml"
                }
            }
        }
    }
    ```
    
# Dealing with secrets and values

Devops-as-code allows you to parameterize your yaml files with the help of values and secrets.
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
  username: !value user
  password: !secret pass
```

There are many ways how you can specify values or secrets:

**Using `<USER_HOME>/.xebialabs/config.yaml`:**
```yaml
secrets:
  pass: qwerty
values:
  user: admin
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
./xlw apply -v -f host.yaml --values=user=admin --secrets=pass=qwerty

# passing multiple values and secrets
./xlw apply -v -f host.yaml --values=user=admin --values=order=1 --secrets=pass=qwerty --secrets=passphrase=secret
```

---
**Using environment variables.**
Any environment variable that starts with `XL_VALUE_` or `XL_SECRET_` will be passed devops-as-code command as a value and secret respectively.<br>

_**Please notice, that variable names are case sensitive**_

```groovy
pipeline {
    agent any
    environment {
        XL_VALUE_user = admin
        XL_SECRET_pass = qwerty
    }

    stages {
        stage("Apply host.yaml") {
            steps {
                sh "./xlw apply -v -f host.yaml"
            }
        }
    }
}
```

# Hashicorp Vault integration

It is possible to inject values / secrets from Hashicorp Vault.

Just follow these simple steps:
* Install [hashicorp-vault-pipeline-plugin](https://github.com/jenkinsci/hashicorp-vault-pipeline-plugin)
* Configure your vault in Jenkins
* Inject data from vault into `XL_VALUE_`, `XL_SECRET_`, `XL_DEPLOY_` or `XL_RELEASE_` environment variables:
    ```groovy
    pipeline {
        agent any
        environment {
            XL_DEPLOY_USERNAME = vault path: 'xl/secrets/xld', key: 'username'
            XL_DEPLOY_PASSWORD = vault path: 'xl/secrets/xld', key: 'password'
            XL_SECRET_AWS_ACCESS_TOKEN = vault path: 'xl/secrets/aws', key: 'token'
            XL_VALUE_BUILD_NUMBER = vault path: 'xl/secrets/nexus', key: 'lastBuildNumber'
        }
    
        stages {
            stage("Apply infrastructure.yaml") {
                steps {
                    sh "./xlw apply -v -f infrastructure.yaml"
                }
            }
        }
    }
    ```