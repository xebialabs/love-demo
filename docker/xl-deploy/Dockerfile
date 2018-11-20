FROM xebialabsunsupported/xl-deploy:8.5.0-alpha.98

COPY default-conf/* /opt/xebialabs/xl-deploy-server/default-conf/
RUN rm -f /opt/xebialabs/xl-deploy-server/default-plugins/xld-aws-plugin-*.xldp
RUN rm -f /opt/xebialabs/xl-deploy-server/default-plugins/xld-kubernetes-plugin-*.xldp
COPY default-plugins/* /opt/xebialabs/xl-deploy-server/default-plugins/
COPY lib/* /opt/xebialabs/xl-deploy-server/lib/
