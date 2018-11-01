# Approach

Taking into account that devops-as-code provides convenient wrapper for *NIX and Windows systems, it is very easy to using together with different CI tools.

To integrate devops-as-code into your git flow, please follow these simple steps:

1) Add wrappers to your project. You can either copy/paste them from another project, or execute `xl wrapper` command in the root of your project to generate them.
2) Define devops-as-code YAML in your project's directory.  
3) Define `bat / sh` step in your `.travis.yaml` and point to your devops-as-code YAML file(s)
    * Windows:
        ```yaml
        os: windows
        script:
          - cmd.exe /c "xlw.bat apply -f xebialabs.yaml"
        ```
    * Linux/Mac:
        ```yaml
        os: linux
        script:
          - ./xlw apply -f xebialabs.yaml
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
Define `XL_DEPLOY_USERNAME, XL_DEPLOY_PASSWORD` for `XLD` and `XL_RELEASE_USERNAME, XL_RELEASE_PASSWORD` for `XLR`
```yaml
os: linux
env:
  - XL_DEPLOY_URL = http://xl-deploy:4516
  - XL_DEPLOY_USERNAME = admin
  - XL_DEPLOY_PASSWORD = qwerty
  
  - XL_RELEASE_URL = http://xl-release:5516
  - XL_RELEASE_USERNAME = admin
  - XL_RELEASE_PASSWORD = qwerty
script:
  - ./xlw apply -f xebialabs.yaml
```

# Dealing with usernames and passwords

Devops-as-code allows you to parameterize your yaml files with the help of values.
Imagine, that you'd like to dynamically inject `username` and `password` into such a yaml file:

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
  password: !value pass
```

There are many ways how you can specify values:

You can specify the values using xlvals files. Please use the extension `.xlvals`, for example put the following values in a file called `secrets.xlvals`:

```properties
user=admin
pass=424242
```

Please make sure to not check in value files that contain sensitive information into version control. The XL Cli searches for value files in `<USER_HOME>/.xebialabs` and in the folder the yaml file is located. If you keep the xlvals file in the project directory, you can add it to the gitignore to prevent the file from being checked in.

---
**Using inline command parameters:**
```bash
./xlw apply -v -f host.yaml --values=user=admin --values=pass=qwerty

# passing multiple values
./xlw apply -v -f host.yaml --values=user=admin --values=order=1 --values=pass=qwerty --values=passphrase=secret
```

---
**Using environment variables.**
Any environment variable that starts with `XL_VALUE_` will be passed devops-as-code command as a value.<br>

_**Please notice, that variable names are case sensitive**_

```yaml
os: linux
env:
  - XL_VALUE_user = admin
  - XL_VALUE_pass = qwerty
script:
  - ./xlw apply -f host.yaml
```

# Using Travis Encrypted keys

If you don't want to store sensitive XLD-related information in raw format, you can use [TravisCi encrypted keys](https://docs.travis-ci.com/user/encryption-keys).

You can encrypt and store some environment variables like this:
```bash
travis encrypt XL_DEPLOY_URL="http://10.0.4.20:4516" --add --com
travis encrypt XL_DEPLOY_USERNAME="admin" --add --com
travis encrypt XL_DEPLOY_PASSWORD="qwerty" --add --com
travis encrypt XL_VALUE_BUILD_NUMBER=5 --add --com
travis encrypt XL_VALUE_TOKEN="secret_token" --add --com
```
Because you use `--add` key, few new lines will be added to your `.travis.yaml` file:

```bash
....
env:
  global:
  - secure: IlLyh/ddhW0ZovzXSldAp...
  - secure: grbKfTp6opi5pu6GvnITR...
  - secure: D0An56kLDqiuV9RjfcnOi...
  - secure: pBV4SF0SrJ4R0oHvOI8Hs...
  - secure: PImx0dm5n0Sql73wNoaSZ...
```

Those values will be decrypted during build and set an an environment variables and `xl` command will pick them up.
