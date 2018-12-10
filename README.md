# This is the DevOps as Code demo repository!!

 The DevOps as Code demo is updated for every DevOps As Code sprint demo. That means it is usually more up-to-date than the DevOps as Code workshop, but it will also be broken more often.

Have a look at the [the DevOps as Code workshop](https://github.com/xebialabs/devops-as-code-workshop) for a more stable experience.


## Install licenses for XL Deploy and XL Release

The demo requires you to bring your own licenses for XL Deploy and XL Release. You can use production licenses or request trial licenses for [XL Deploy](https://xebialabs.com/products/xl-deploy/trial/) and  [XL Release](https://xebialabs.com/products/xl-release/trial/).

1) Copy the XL Deploy license to `docker/xl-deploy/default-conf/deployit-license.lic`

2) Copy the XL Release license to `docker/xl-release/default-conf/xl-release-license.lic`

## Start up the XL DevOps Platform

1) If you are already running XL Deploy or XL Release on your local machine, please stop them.

2) If you are running the workshop on Windows, execute the following command to be able to run the Docker Compose file:

```
> set COMPOSE_CONVERT_WINDOWS_PATHS=1
```

For more information on this environment variable, read [the documentation for Docker Compose](https://docs.docker.com/compose/reference/envvars/#compose_convert_windows_paths)

3) Start up the XL DevOps Platform:

```
$ docker-compose up --build
```

4) Wait for XL Deploy and XL Release to have started up. This will have occurred when the following line is shown in the logs:
```
devops-as-code-demo-cli_1 exited with code 0
```

5) Open the XL Deploy GUI at http://localhost:4516/ and login with the username `admin` and password `admin`. Verify that the about box reports the version to be **8.5.0**.

6) Open the XL Release GUI at http://localhost:5516/ and login with the username `admin` and password `admin`. Verify that the about box reports the version to be **8.5.0**.

## Install the XL CLI

1) Open a new terminal window and install the XL command line client:

### Mac
```
$ curl -LO https://xl-cli.s3.amazonaws.com/bin/8.5.0/darwin-amd64/xl
$ chmod +x xl
$ sudo mv xl /usr/local/bin
```

### Linux
```
$ curl -LO https://xl-cli.s3.amazonaws.com/bin/8.5.0/linux-amd64/xl
$ chmod +x xl
$ sudo mv xl /usr/local/bin
```

### Windows
Download https://xl-cli.s3.amazonaws.com/bin/8.5.0/windows-amd64/xl.exe
and place it somewhere on your `%PATH%`

2) Run the following command to verify that you have the right version of the XL CLI installed:

```
$ xl version
```

The output should look like this:
```
CLI version:             8.5.0
Git version:             8.5.0-0-g2d5a36c
API version XL Deploy:   xl-deploy/v1
API version XL Release:  xl-release/v1
Git commit:              2d5a36cd5769ea59b0ac4e11e4709d6504381076
Build date:              2018-12-05T14:01:24.212Z
GO version:              go1.11
OS/Arch:                 darwin/amd64
```

The last line will be different, depending on the architecture of your machine.
