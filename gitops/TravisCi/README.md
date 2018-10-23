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

# Dealing with secrets and values

Devops-as-code allows you to parameterize your yaml files with the help of values and secrets.
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

```yaml
os: linux
env:
  - XL_VALUE_user = admin
  - XL_SECRET_pass = qwerty
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
travis encrypt XL_SECRET_TOKEN="secret_token" --add --com
```
Because you use `--add` key, few new lines will be added to your `.travis.yaml` file:

```bash
....
env:
  global:
  - secure: IlLyh/ddhW0ZovzXSldAp/xiFR9IQA2uZAH22W80VLhRuBwPksRLkQ5+4pfzcLBjLK7IIUm+6LuF9Qx8HE+ZNLRl/E+j9A5TsCIHumEdQ3bjzy3bpEquaW1PTd4gNcB4g57Eom9E9Rfi4+0YFAygA6p+uEqzfNo/4sLjjzsg+Vel0+6s0OipMqibkXR0hcyJvOta4qa5qUs3wLqcbulpnFNRSvcUXuOAeWmHnJo0iG4mrDej2iyvpSM7ab353gSnyKUL+zX0+qrFLuhfn1iHAKSbuGT+HVSn+L+yokTdXfY/yDshqIaVS6sLx93BCfDxDkbGhPhTeLEaWZe2QdS4keSlqAu5I20rARDK/l6mU1RItaHJOIMq5mgp5QglqCrlVkiuwiLXvn9CWhK+FRT4cUuFrImv39aDlFKPCZflzX4lv+3QlD+eFhJ24QRQXZn4aRzd8l2w1dz8OiiXcg3CksfDfmPBhvJc+zcS6ZaT/4FaaYo8IIV78/rEEerHnR0SVxVxDXja/R2TbhkeISUIkbs9a8NjE1/mwgJDpCG5WHrFOEZC7AfIohKBsSXPQ0aAUnPEHDoClScSau/j2yiXCnZsdk6vyjYQOKQDQy/B6YDpOKs/fzb9+o209BLihqrAiAamP1NagqcJ2UNWUmy9I3gr9SvZhuX++H4e4ZaQvcg=
  - secure: grbKfTp6opi5pu6GvnITRNKCM5UOvMXSTDmowi5aJvrv9czhCe6s760NBfCqc84g+oSGhglbT9SEWKkvdMQlU7s7zQYFTYWMTRW2jKZH/BDam2TBnvuDNVnF3VWPfttPABP5HYAVr8NMib4Jz1NdXjC7gMdkJCVRmfvKA+dMheckO/qnU1qhGfjUutja1tXpFr1hXHpJXrmUoqBpbDEw1F2GIxLsNC2vQxwxRQapFezCI2YUAhkiY3F79Yf9EApLr7S9KfR1ynQ/Ppg5YV9hF/RfGNJsuBEkkqHO6geygoUmF+mnpApxRqPfCi6N/v16NAJ1nbFnUAeFCkCuSg2sWRpqjoW1Fuf3v8TKZ7r4sXxDv4FseMadfsMtLq4czrZae+XaJkrTk6Tness6FqoLD4mHhlM2mPz5gNiPGIsGxeWMTCdPlK20PO2u92mhJkr3JIPkf8+vXF2u5eUw/k/F9H/P1ICUjKHEi6+8I5WPuisyPRR3YxHxx2Z7Wt3IzOaTjIO4gJkW1YoNgGkMjbLHR36YjDmEMnPJf5bheyIZlgLBCIgE4WaDe3IshGE5yrRDRfbl2cL3wEp52OK84WhuoNqYBOVsKpwlFv2ZJ03bbivgDQ82zSsR9Tg1TsQ2s2jYfW9i2mV7CSaLwiltQg5qazzmsy4K07fNxJcdjBFItNs=
  - secure: D0An56kLDqiuV9RjfcnOisk7uMgD7RvlZkdLSYgRir5Ab5BMzK9eGvKYRZSpOPTwSaeByckxQ6vBXl2ozgfBa/FAQ1Hk6TeL0mzvyz0IyOJVWSHgf0PYS8isZ4N+CRR3LLdbvjav7D7mU4RehCo1JRtSmytaEngZEjx7zViyJ1csu3yzq4BEqavCPj6Nwf+tzd+LKZ/qVqabTzbpDSdVaHP3YB1kB6q+z7bvvZgA218qvzv7nvm2OmgL9uLiT0f7lAtEo9dH2Zj8TcUvwhYxJsSBDwNkYu66HvQV0hw2DaG6Ao68kIblQWcvZBTOQ2B4wG2ORXBuZUJCbGQOeXVyRFw13juUv8r76BxoxT7cNitEgSG1rM7C0bDAc1FT7fMZRhOdqKh5Nccxj8iLvyzoTqgj17mm7FRqAdXVIBjOPaCFYz+WW87oWnZ5/6ofYK2af580pctFllwhSTQngMbFr7+jM/k03vKTBNq4FrBBx8V7ipvZVUNLYEgv5XSxvaeo17sf3qlNAnvPeJlnSVqE99/dCN0zCFKxfbgsAuLi3fXtJ+zBx39mGBWz39d33Lpisuo6C4676IwpIs3aZJPfyXn6np8ZWQxLDMfq6vBv2hFMzVwBn7miwwB0w5DKmZxZioGNU7Af0wHvhXnqJUbJ5lQ7D6YIFlk3Wh5pH84nM2o=
  - secure: pBV4SF0SrJ4R0oHvOI8Hs07/Ll8RUVW4OYDhJC5tgqWzl5b1ig3X4VPzPS2xnta5eZFFlyIzOAdiJb5l4bqmnYwY/acXDVbv1Ih8Vijlrn+i5YOUiIJz8EPWOvNsOAHHFOl5pDgkK48IlHVtoDHJK+LDOqmLsbU/igRyEckir8VfFaSjDIz0weEezOnXOeX8JH5+GzfSCxQ0WaxBK8URnG4npg++Hehy6zlvYY9WGxZmiTp+u60rtohbj1RjT3Gg+6kr+/WJDa42QSjyPD9EZVAKM4KyEEMVaU9KuPDOYO7tru/Xl5zFRJFXX+JENNL4VzaS6SJfQIwXSMimh+3GLtf4eytPIIvNKh8TFKGNsHoj4hDMTIKE+ggTiiQAnjjlHTE+oypRgyQAyynLoHogwJ6pD4bi8oS5ooJXyVl+Ro7eW+RbVtKuLttNgeXWySjCzpkF10Np6HuVHTQYF83fwk+W9b2TVOF72AlqfDjxo8Fl5+MJ+KRcQr9Q23quCIbu5uwJnej+E6vWwQEdnuBlU9m0ZgUUmwnueVndSvXik1hfGwtN+2CzGlR+yLqjZMx793e0b2+taYWZw8d6jaIaAaPrR+yGR+VlNvUS4yb9y3fMlmTk6pKHA1e7oY/XmJ34ekyhKe+NQ1K3qUdI74ZderJh9a79w1tEC00tJhBps9g=
  - secure: PImx0dm5n0Sql73wNoaSZqD1KfGZ8e9KlvOgjX/KLtNUH5Tm2iVXnX3Ej6+3QdZb7kOHlH39Kp+lIn88cG7qqG5MBKVBRhWU0UJfXmd4AY0hzppp3TbCjJ43mgsj4scXAferr3NunAI6RmP1JbviyWds9tcoKBuwJWH3vL3lI2zV6X4kIWp19r+yfFMz03i3m4VillBDadDRnTUiboAyxXRKdNbw1kZvwO17rjIRKI3Ur6HRDVM4ZQw1bGnVmytAS/u+fuevqg+ziKw+ZVbLk04swojso40whAsYMQzoLEtLuFuwMdZUondy8cSDqFWtNS43sWecFrPmNIu/z1vFmqG4h3ppxR1B/z6Hl/EjmvFmsslilOrjdJLQFbmMl6llEyRy0cOgIc2bcktA/qaCifYbj4FzhENiKQPSzCJHHqPt0jzmxKRdMpcqfckxIJpOGbbpzMe5GdbQzTIpGL8Lxxyp3KAY1xOvxB2SvglxoUz4jqEmElqBNF1u4wvfvQrrrS/iR/PwNVEhfS3MENDTnYgDdK/rWeGe4LZJ2ycwP+3cjm+FQ1HFqlAQhO/h/HSqTyvEBOpYlaKrHswPtdkIg+jPKsELyK4/8MPSb+7vG/b+IITjwR1G6530gRkpbuVodLkiOHxt12xVMTzM9UJHS/vliJpc8mL05FD+FgIP3IA=
```

Those values will be decrypted during build and set an an environment variables and `xl` command will pick them up.
