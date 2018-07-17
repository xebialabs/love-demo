stage { 'preinstall':
        before => Stage['main']
        }

class apt_get_update {
	exec { 'apt-get -y update':
	command => '/usr/bin/apt-get -y update',
	path => '/usr/bin',
	}
}

class { 'apt_get_update':
	stage => preinstall
}

class { 'mysql::server':
  root_password => 'password',
  override_options => {
        mysqld => { bind_address => '0.0.0.0'}
      },
}

mysql::db{ ['restaurant']:
  ensure  => present,
  user => 'app_user',
  host => '%',
  password => 'password',
  charset => 'utf8',
  require => Class['mysql::server'],
}