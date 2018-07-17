stage { 'preinstall':
  before => Stage['main']
}

class apt_get_update {
  exec { 'apt-get -y update':
    command => '/usr/bin/apt-get -y update',
    path    => '/usr/bin',
  }
}

class { 'apt_get_update':
  stage => preinstall
}

include ::apache
include ::apache::mod::proxy
include ::apache::mod::proxy_http


class { 'tomcat':
  user => 'ubuntu',
}
class { 'java8': }
tomcat::instance { 'rest-o-rant':
    source_url => 'https://archive.apache.org/dist/tomcat/tomcat-7/v7.0.81/bin/apache-tomcat-7.0.81.tar.gz'
}->
tomcat::service { 'default': }
