FROM xebialabs/xl-cli:8.2.0-alpha.2

USER 0
COPY resources/wait-for /usr/local/bin
RUN chmod +x /usr/local/bin/wait-for
USER 10001

ENTRYPOINT ["/usr/local/bin/wait-for", "-t", "120", "xl-deploy:4516", "--", "/usr/local/bin/wait-for", "-t", "120", "xl-release:5516", "--", "/usr/local/bin/xl"]
