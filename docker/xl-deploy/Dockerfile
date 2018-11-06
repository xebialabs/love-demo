FROM xl-docker.xebialabs.com:443/xl-deploy:8.5.0-alpha.65

COPY default-conf/* /opt/xebialabs/xl-deploy-server/default-conf/
RUN rm -f /opt/xebialabs/xl-deploy-server/default-plugins/xld-aws-plugin-*.xldp
COPY default-plugins/* /opt/xebialabs/xl-deploy-server/default-plugins/
COPY lib/* /opt/xebialabs/xl-deploy-server/lib/
