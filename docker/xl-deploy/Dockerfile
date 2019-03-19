FROM xebialabs/xl-deploy-internal:8.6

# Add license file
COPY default-conf/* /opt/xebialabs/xl-deploy-server/default-conf/

# Add latest plugin builds
RUN rm -f /opt/xebialabs/xl-deploy-server/default-plugins/xld-aws-plugin-*.xldp
RUN rm -f /opt/xebialabs/xl-deploy-server/default-plugins/xld-terraform-plugin-*.xldp
COPY default-plugins/* /opt/xebialabs/xl-deploy-server/default-plugins/

# Add latest DevOps as Code build
# COPY lib/* /opt/xebialabs/xl-deploy-server/lib/
