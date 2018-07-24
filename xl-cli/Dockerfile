FROM alpine:3.7

RUN apk add --no-cache curl

RUN curl -o /usr/local/bin/xl https://s3.amazonaws.com/xl-cli/com/xebialabs/xl-cli/8.2.0-alpha.1/xl-cli-8.2.0-alpha.1-linux_amd64_xl.bin && \
    chmod +x /usr/local/bin/xl

RUN curl -o /usr/local/bin/wait-for https://raw.githubusercontent.com/eficode/wait-for/master/wait-for && \
    chmod +x /usr/local/bin/wait-for

USER 10001
VOLUME "/data"

ENTRYPOINT ["/usr/local/bin/wait-for", "-t", "120", "xl-deploy:4516", "--", "/usr/local/bin/wait-for", "-t", "120", "xl-release:5516", "--", "/usr/local/bin/xl"]
