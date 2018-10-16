FROM jenkins/jenkins:2.138.1
COPY init.groovy /var/jenkins_home/init.groovy.d/
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt

ENV JENKINS_USER admin
ENV JENKINS_PASS admin

ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false -Djenkins.model.Jenkins.slaveAgentPort=55888